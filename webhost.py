from flask import Flask, render_template, send_file

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/scripts/<script>")
def load_script(script: str):
    return send_file(f"scripts/{script}", mimetype="application/javascript")


@app.route("/files/<file>")
def load_file(file: str):
    match file.split(".")[1]:
        case "mp4":
            mimetype = "video/mp4"
        case _:
            mimetype = "text/plain"

    return send_file(f"files/{file}", mimetype=mimetype)


app.run(debug=True)
