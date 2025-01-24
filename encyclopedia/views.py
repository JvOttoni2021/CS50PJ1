from django.shortcuts import render

from . import util


def index(request):
    full_list = util.list_entries()
    shown_list = list()

    if request.method == "POST":
        search = request.POST.get('q')

        search_page_content = util.get_entry(search)

        if search_page_content is not None:
            return shows_content(request, search)

        shown_list = util.list_entries(search)

    if len(shown_list) == 0:
        shown_list = full_list

    return render(request, "encyclopedia/index.html", {
        "entries": shown_list
    })

def shows_content(request, page_title):
    return render(request, "encyclopedia/content.html", {
        "page_body": util.get_entry(page_title),
        "title": page_title.capitalize()
    })
