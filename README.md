### sanic_compress

sanic_compress is an extension which allows you to easily gzip your Sanic responses. It is a port of the [Flask-Compress](https://github.com/libwilliam/flask-compress) extension.


## Installation

Install with `pip`:

`pip install sanic_compress`

## Usage

Usage is simple. Simply pass in the Sanic app object to the `Compress` class, and responses will be gzipped.

```python
from sanic import Sanic
from sanic_compress import Compress

app = Sanic(__name__)
Compress(app)
```

Alternatively, if you want to initialize the `Compress` class later, you can do so with the `init_app` method;

```python
compress = Compress()
app = Flask(__name__)
compress.init_app(app)
```


## Options

Within the Sanic application config you can provide the following settings to control the behavior of sanic_compress. None of the settings are required.

| Option | Description | Default |
| ------ | ----------- | ------- |
| `COMPRESS_MIMETYPES` | Set the list of mimetypes to compress here. | `[`<br>`'text/html',`<br>`'text/css',`<br>`'text/xml',`<br>`'application/json',`<br>`'application/javascript'`<br>`]` |
| `COMPRESS_LEVEL` | Specifies the gzip compression level (1-9). | `6` |
| `COMPRESS_MIN_SIZE` | Specifies the minimum file size threshold for compressing files. | `500` |

A higher `COMPRESS_LEVEL` will result in a gzipped response that is smaller, but the compression will take longer.

Example of using custom configuration:

```
from sanic import Sanic
from sanic_compress import Compress

app = Sanic(__name__)
app.config['COMPRESS_MIMETYPES'] = set(['text/html', 'application/json'])
app.config['COMPRESS_LEVEL'] = 4
app.config['COMPRESS_MIN_SIZE'] = 300
Compress(app)
```

### Note about gzipping static files:

Sanic is not at heart a file server. You should consider serving static files with nginx or on a separate file server.