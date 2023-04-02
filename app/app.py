from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('./app/data/data.json') as json_file:
        data = json.load(json_file)
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
