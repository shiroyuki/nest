modules = dict()

{% for id in modules %}
modules['{{ id }}'] = {{ modules[id] }}
{% endfor %}

if __name__ == '__main__':
    console = Console()

    for id in modules:
        console.enable(id, modules[id])

    console.run()