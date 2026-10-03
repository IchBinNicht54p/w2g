from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scripts/<script>")
def load_script(script: str):
    return send_file(f"scripts/{script}", mimetype="application/javascript")


app.run(debug=True)
