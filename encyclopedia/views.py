from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def shows_content(request, page_title):
    return render(request, "encyclopedia/content.html", {
        "page_body": util.get_entry(page_title),
        "title": page_title.capitalize()
    })
