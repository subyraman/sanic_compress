import pytest
from sanic import Sanic
from sanic.response import html, json, HTTPResponse
from sanic_compress import Compress

OTHER_COMPRESSIBLE_TYPES = set([
    'text/css',
    'application/javascript'])

BUNCH_OF_TYPES = OTHER_COMPRESSIBLE_TYPES.union([
    'image/png', 'application/pdf', 'image/jpeg',
])

CONTENT_LENGTHS = [100, 499, 500]
HEADERS = [
    {'Accept-Encoding': 'gzip'},
    {'Accept-Encoding': ''}
]

STATUSES = [200, 201, 400, 401, 500]

VARY_HEADERS = ['Accept-Encoding', 'Referer', 'Cookie']


@pytest.fixture
def compressed_app():
    app = Sanic('compressed')
    Compress(app)

    @app.route('/json/<length>')
    def j(request, length):
        data = {'a': "".join(['b'] * (int(length) - 8))}
        return json(data)

    @app.route('/html/<length>')
    def h(request, length):
        res = "".join(['h' for i in range(int(length))])
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

    return app


@pytest.mark.parametrize('headers', HEADERS)
@pytest.mark.parametrize('content_length', CONTENT_LENGTHS)
def test_sets_gzip_for_html(compressed_app, headers, content_length):
    request, response = compressed_app.test_client.get(
        '/html/{}'.format(content_length), headers=headers)

    if ('gzip' in headers.get('Accept-Encoding') and
            content_length >= compressed_app.config['COMPRESS_MIN_SIZE']):
        assert response.headers['Content-Encoding'] == 'gzip'
        assert response.headers['Content-Length'] < str(content_length)
    else:
        assert response.headers['Content-Length'] == str(content_length)
        assert 'Content-Encoding' not in response.headers


@pytest.mark.parametrize('headers', HEADERS)
@pytest.mark.parametrize('content_length', CONTENT_LENGTHS)
def test_gzip_for_json(compressed_app, headers, content_length):
    request, response = compressed_app.test_client.get(
        '/json/{}'.format(content_length), headers=headers)

    if ('gzip' in headers.get('Accept-Encoding') and
            content_length >= compressed_app.config['COMPRESS_MIN_SIZE']):
        assert response.headers['Content-Encoding'] == 'gzip'
        assert response.headers['Content-Length'] < str(content_length)
    else:
        assert response.headers['Content-Length'] == str(content_length)
        assert 'Content-Encoding' not in response.headers


@pytest.mark.parametrize('headers', HEADERS)
@pytest.mark.parametrize('content_length', CONTENT_LENGTHS)
@pytest.mark.parametrize('content_type', BUNCH_OF_TYPES)
def test_gzip_for_others(
        compressed_app, content_type, headers, content_length):
    request, response = compressed_app.test_client.get(
        '/other/{}'.format(content_length), headers=headers,
        params={'content_type': content_type})

    if ('gzip' in headers.get('Accept-Encoding') and
            content_length >= compressed_app.config['COMPRESS_MIN_SIZE']
            and content_type in OTHER_COMPRESSIBLE_TYPES):
        assert response.headers['Content-Encoding'] == 'gzip'
        assert response.headers['Content-Length'] < str(content_length)
    else:
        assert response.headers['Content-Length'] == str(content_length)
        assert 'Content-Encoding' not in response.headers


@pytest.mark.parametrize('status', STATUSES)
def test_no_gzip_for_invalid_status(compressed_app, status):
    request, response = compressed_app.test_client.get(
        '/html/status/{}'.format(status),
        headers={'Accept-Encoding': 'gzip'})

    if status < 200 or status >= 300:
        assert 'Content-Encoding' not in response.headers
    else:
        assert response.headers['Content-Encoding'] == 'gzip'


def test_gzip_levels_work(compressed_app):
    prev = None
    for i in range(1, 10):
        compressed_app.config['COMPRESS_LEVEL'] = i

        request, response = compressed_app.test_client.get(
            '/html/501',
            headers={'Accept-Encoding': 'gzip'})

        if prev:
            print(response.headers['Content-Length'])
            assert response.headers['Content-Length'] < prev,\
                'compression level {} should be smaller than {}'.format(
                    i, i-1
                )


@pytest.mark.parametrize('vary', VARY_HEADERS)
def test_vary_header_modified(compressed_app, vary):
    request, response = compressed_app.test_client.get(
            '/html/vary/{}'.format(vary),
            headers={
                'Accept-Encoding': 'gzip',
            })

    if vary:
        if 'accept-encoding' not in vary.lower():
            assert response.headers['Vary'] == '{}, Accept-Encoding'.format(
                vary)
    else:
        assert response.headers['Vary'] == 'Accept-Encoding'
