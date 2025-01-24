from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
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


class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the page title...'
        }))
    page_content = forms.CharField(
        label="Page Content",
        widget=forms.Textarea(attrs={
            'rows': 5,
            'cols': 80,
            'placeholder': 'Enter the content of the page here...'
        })
    )

    def __init__(self, *args, title="", page_content="", **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].initial = title
        self.fields['page_content'].initial = page_content
        self.check_title(title=title)
    
    def check_title(self, title):
        if title != "":
            self.fields['title'].widget.attrs.update({
                'hidden': 'hidden',
            })

            self.fields['title'].label = ''


def edit(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            form_title = form.cleaned_data["title"]
            page_content = form.cleaned_data["page_content"]
            util.save_entry(form_title, page_content)
            return redirect(reverse("shows_content", args=[form_title]))


    return render(request, "encyclopedia/edit.html", {
        "form": NewPageForm(title=title, page_content=util.get_entry(title)),
        "result_message": "",
        "title": title
    })


def add(request):
    if request.method == "POST":
        result_message = ""
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            search_page_content = util.get_entry(title)

            if search_page_content is None:
                page_content = form.cleaned_data["page_content"]

                util.save_entry(title, page_content)
                return shows_content(request, title)
            else:
                result_message = f"Page \"{title}\" already exists!"

        return render(request, "encyclopedia/add.html", {
            "form": form,
            "result_message": result_message
        })
        
    return render(request, "encyclopedia/add.html", {
        "form": NewPageForm(),
        "result_message": ""
    })
