from flask import Flask
from flask import render_template as render

app_name = '{{ name }}'

app = Flask(__name__)

@app.route("/")
def index():
    return render('index.html', name = app_name)

if __name__ == "__main__":
    options = {
        'host':  '0.0.0.0',
        'debug': True,
        'port':  {{ port }}
    }

    app.run(**options)