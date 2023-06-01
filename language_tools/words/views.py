import json
import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseBadRequest
from django.http.request import QueryDict
from django.shortcuts import HttpResponse, render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def index(request: WSGIRequest):
    return render(request,"words/index.html")

@require_http_methods(["POST"])
def words2mp3(request: WSGIRequest):
    request_body_args: QueryDict = request.POST

    # words列表
    words = request_body_args.get("words",None)
    # word循环次数
    loop = request_body_args.get("loop",None)
    # word播放速度
    speed = request_body_args.get("speed",None)

    # check
    if not speed:
        return HttpResponseBadRequest("error")
    if not loop:
        return HttpResponseBadRequest("error")
    if not words:
        return HttpResponseBadRequest("error")
    
    try:
        words_list: list[str] = json.loads(words)
        loop: int = int(loop)
        speed: float = float(speed)
    except TypeError:
        return HttpResponseBadRequest("error")
    
    logging.warning(f"post: {words_list} {loop} {speed} {type(words_list)} {type(loop)} {type(speed)}")

    # 同步生成
    # TODO 根据words列表生成mp3
    # TODO 将mp3拼接成audio
    return HttpResponse("ok")

