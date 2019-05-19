from sanic import Sanic
from sanic.response import json, html, HTTPResponse
from sanic_compress import Compress

app = Sanic('compressed')
Compress(app)


@app.route('/json/<length>')
def j(request, length):
    data = {'a': "".join(['b'] * (int(length) - 8))}
    return json(data)


@app.route('/ping/<cnt_pong:int>')
def ping(request, cnt_pong):
    """ Handler to get humanity result"""
    return json({"success": True, "result": ["pong"] * cnt_pong})


@app.route('/')
def h(request):
    res = "".join(['h' for i in range(int(501))])
    return html(res)


@app.route('/html/status/<status>')
def h_with_status(request, status):
    res = "".join(['h' for i in range(501)])
    return html(res, status=int(status))


@app.route('/html/vary/<vary>')
def h_with_vary(request, vary):
    res = "".join(['h' for i in range(501)])
    return html(res, headers={'Vary': vary})


@app.route('/other/<length>')
def other(request, length):
    content_type = request.args.get('content_type')
    body = "".join(['h' for i in range(int(length))])
    return HTTPResponse(
        body, content_type=content_type)

app.run()