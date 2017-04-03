import os
from django.http import HttpResponse
from .forms import NameForm
from . import searcher_settings, search


def main(request):
    resp = \
        u"""<!DOCTYPE HTML>
    <html>
        <head>
            <meta charset="utf-8">
        <title>TEST</title>
        </head>
        <body>
        <h1>
        <form action="/process/" method="post">
            <label for="process">Search: </label>
            <input id="process" type="text" name="process" value="">
            <input type="submit" value="OK">
        </form>
        </h1>
        </body>
    </html>
    """
    return HttpResponse(resp)


def process(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    output = 'RESULTS:<br>'
    # query is request.POST['process']
    sch = search.search(defaultpath=searcher_settings.PATH, jsonFile=searcher_settings.JSON_NAME)
    filesDict = sch.main(request.POST['process'])
    for file in filesDict:
        output += str(file).split(searcher_settings.SEPARATOR)[len(str(file).split(searcher_settings.SEPARATOR)) - 1
                                                               ].replace(searcher_settings.DATA_FILES_EXTENSION, '') + \
                  '<br>'
    resp = \
        u"""<!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
    <title>TEST</title>
    </head>
    <body>
    <h1>
    <form action="/process/" method="post">
        <label for="process">Search: </label>
        <input id="process" type="text" name="process" value="">
        <input type="submit" value="OK">
    </form>
    </h1>
    <h3>YOU SEARCHED:<br> {0}</h3>
    </body>
    </html>""".format(output)

    print(request.POST)
    return HttpResponse(resp)
