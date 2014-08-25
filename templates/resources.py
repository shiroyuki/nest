import base64
import zlib

resources = dict()

{% for name in resources %}
resources['{{ name }}'] = zlib.decompress(base64.b64decode('{{ resources[name] }}'))
{% endfor %}