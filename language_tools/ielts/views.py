import json
import logging

from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.http import HttpResponseBadRequest
from django.http.request import QueryDict
from django.shortcuts import HttpResponse, render
from django.views.decorators.http import require_http_methods

from .models import BookModel, ChapterModel, PaperModel, WordModel


@require_http_methods(["GET"])
def index(request: WSGIRequest):
    BookModel.objects.all()
    corpus_listen: dict ={
        "books":BookModel.objects.all()
    }
    return render(request,"ielts/index.html",context={"corpus_listen":corpus_listen})

@require_http_methods(["GET"])
def get_chapters(request,book_id: str):
    chapters: QuerySet = BookModel.objects.get(id=book_id).chapters.all()
    res = [{"id":chapter.id,"name":chapter.name} for chapter in chapters]
    logging.warning(f"{res} {type(res)}")
    return HttpResponse(json.dumps(res))

@require_http_methods(["GET"])
def get_papers(request,chapter_id: str):
    papers: QueryDict = ChapterModel.objects.get(id=chapter_id).papers.all()
    res = [{"id":paper.id,"name":paper.name} for paper in papers]
    return HttpResponse(json.dumps(res))

@require_http_methods(["POST"])
def corpus_listen_check(request: WSGIRequest):
    request_body_args: QueryDict = request.POST
    book_id = request_body_args.get("book",None)
    chapter_id = request_body_args.get("chapter",None)
    paper_id = request_body_args.get("paper",None)
    content = request_body_args.get("content",None)

    # check
    if (not book_id) or (not chapter_id) or (not paper_id) or (not content):
        return HttpResponseBadRequest("error")
    
    try:
        book_id: int = int(book_id)
        chapter_id: int = int(chapter_id)
        paper_id: int = int(paper_id)
        content: list[str] = json.loads(content)
    except TypeError:
        return HttpResponseBadRequest("error")
    
    # get all answer data
    # 查询. 非接口形式，不需要验证
    paper: PaperModel = BookModel.objects.get(id=book_id).chapters.get(id=chapter_id).papers.get(id=paper_id)
    words: QuerySet = paper.words.all()
    words: list[str] = [word.name for word in words]
    res = []
    for word in content:
        if word not in words:
            res.append({"en":word,"status":"error"})
        else:
            res.append({"en":word,"status":"ok"})
    
    # 补充缺少的
    loss = list(set(words) - set(content))

    # 存在就正确
    return HttpResponse({"res":res,"loss":loss})
