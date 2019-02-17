from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object('config.default')
app.config.from_envvar('APP_CONFIG_FILE')


@app.route('/')
def hello():
    return jsonify({'message': 'index'})
