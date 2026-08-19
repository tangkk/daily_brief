# -*- coding: utf-8 -*-
import base64
import hashlib
import hmac
import json
import os
import time
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time

import websocket


DEFAULT_URL = "wss://cbm01.cn-huabei-1.xf-yun.com/v1/private/mcd9m97e6"
DEFAULT_VOICE = "x6_lingyuyan_pro"


class WsParam:
    def __init__(self, appid, api_key, api_secret, text, voice, speed=50, volume=52, pitch=50):
        self.appid = appid
        self.api_key = api_key
        self.api_secret = api_secret
        self.text = text
        self.voice = voice
        self.common_args = {"app_id": appid, "status": 2}
        self.business_args = {
            "tts": {
                "vcn": voice,
                "volume": int(volume),
                "rhy": 0,
                "speed": int(speed),
                "pitch": int(pitch),
                "bgs": 0,
                "reg": 0,
                "rdn": 0,
                "audio": {
                    "encoding": "lame",
                    "sample_rate": 24000,
                    "channels": 1,
                    "bit_depth": 16,
                    "frame_size": 0,
                },
            }
        }
        self.data = {
            "text": {
                "encoding": "utf8",
                "compress": "raw",
                "format": "plain",
                "status": 2,
                "seq": 0,
                "text": base64.b64encode(text.encode("utf-8")).decode("utf-8"),
            }
        }


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema


def parse_url(request_url):
    stidx = request_url.index("://")
    host = request_url[stidx + 3 :]
    schema = request_url[: stidx + 3]
    edidx = host.index("/")
    path = host[edidx:]
    host = host[:edidx]
    return Url(host, path, schema)


def assemble_ws_auth_url(request_url, method="GET", api_key="", api_secret=""):
    u = parse_url(request_url)
    date = format_date_time(time.time())
    signature_origin = f"host: {u.host}\ndate: {date}\n{method} {u.path} HTTP/1.1"
    signature_sha = hmac.new(
        api_secret.encode("utf-8"),
        signature_origin.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    signature_b64 = base64.b64encode(signature_sha).decode("utf-8")
    authorization_origin = (
        f'api_key="{api_key}", algorithm="hmac-sha256", '
        f'headers="host date request-line", signature="{signature_b64}"'
    )
    authorization = base64.b64encode(authorization_origin.encode("utf-8")).decode("utf-8")
    return request_url + "?" + urlencode({"host": u.host, "date": date, "authorization": authorization})


def run_once(out_path, text, voice=DEFAULT_VOICE, speed=50, volume=52, pitch=50, requrl=DEFAULT_URL):
    appid = os.environ.get("XFYUN_APPID", "")
    api_secret = os.environ.get("XFYUN_API_SECRET", "")
    api_key = os.environ.get("XFYUN_API_KEY", "")
    if not (appid and api_key and api_secret):
        raise RuntimeError("Missing XFYUN_APPID/XFYUN_API_KEY/XFYUN_API_SECRET")

    ws_param = WsParam(appid, api_key, api_secret, text, voice, speed, volume, pitch)
    ws_url = assemble_ws_auth_url(requrl, "GET", api_key, api_secret)

    frames = {}
    frame_counter = {"value": 0}
    done = {"ok": False, "err": None}

    def on_message(ws, message):
        try:
            msg = json.loads(message)
            header = msg.get("header", {})
            code = header.get("code", -1)
            if code != 0:
                done["err"] = f"code={code}, msg={header.get('message')}, sid={header.get('sid')}"
                ws.close()
                return

            audio_obj = msg.get("payload", {}).get("audio")
            if audio_obj:
                audio_b64 = audio_obj.get("audio", "")
                if audio_b64:
                    seq = audio_obj.get("seq")
                    if seq is None:
                        seq = frame_counter["value"]
                    frame_counter["value"] += 1
                    frames[int(seq)] = base64.b64decode(audio_b64)
                if audio_obj.get("status") == 2:
                    done["ok"] = True
                    ws.close()
        except Exception as exc:
            done["err"] = str(exc)
            ws.close()

    def on_error(ws, error):
        done["err"] = str(error)

    def on_open(ws):
        payload = {"header": ws_param.common_args, "parameter": ws_param.business_args, "payload": ws_param.data}
        ws.send(json.dumps(payload, ensure_ascii=False))

    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error)
    ws.on_open = on_open
    ws.run_forever()

    if done["err"]:
        raise RuntimeError(done["err"])
    if not done["ok"]:
        raise RuntimeError("TTS did not complete")
    if not frames:
        raise RuntimeError("TTS returned no audio frames")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "wb") as f:
        for seq in sorted(frames):
            f.write(frames[seq])

    return out_path
