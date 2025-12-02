from flask import Flask, render_template
import config
from endpoint import endpoint

app = Flask(__name__)
app.register_blueprint(endpoint)

@app.get('/')
def index():
    return render_template('index.html', titulo='Landing page')



if __name__ == '__main__':
    app.run(host=config.host, port=config.port)