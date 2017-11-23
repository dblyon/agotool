from flask import Flask, render_template_string
from flask.ext.profile import Profiler

app = Flask(__name__)
# Flask-Profile is only actived under debug mode
app.debug = True
Profiler(app)

@app.route('/')
def index():
    return render_template_string('<html><body>hello</body></html>')

if __name__ == "__main__":
    app.run()