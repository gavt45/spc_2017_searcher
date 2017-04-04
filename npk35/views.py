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


def content(request, filename):
    resp = """<!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
    <title>TEST</title>
    </head>
    <body>
    <h1>""" + filename + """:</h1>
    <h4>"""
    f = open(searcher_settings.PATH + "files/" + filename + searcher_settings.DATA_FILES_EXTENSION, mode='r',
             encoding='utf-8')
    resp = resp + f.read() + """</h4>
    <a href=\"""" + searcher_settings.NGROK_URL + """\">На главную</a><br>
    </body>
    </html>"""
    f.close()
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
    if not str(request.POST).__contains__("process"):
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
        <h4>Request is blank!</h4>
        </body>
        </html>""".format(output)
        return HttpResponse(resp)

    sch = search.search(defaultpath=searcher_settings.PATH, jsonFile=searcher_settings.JSON_NAME)
    filesDict = sch.main(request.POST['process'])

    if not filesDict:
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
        <h4>Sorry, there is no results for your search!</h4>
        </body>
        </html>""".format(output)
        return HttpResponse(resp)

    for file in filesDict:
        filename = str(file).split(searcher_settings.SEPARATOR)[len(str(file).split(searcher_settings.SEPARATOR)) - 1
                                                                ].replace(searcher_settings.DATA_FILES_EXTENSION, '')
        output += "<a href=\"" + searcher_settings.NGROK_URL + "viewContent/" + filename + "\">" + filename + '</a><br>'
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
