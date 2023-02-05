from flask import Flask, render_template, request, redirect

app = Flask(__name__, static_folder='static')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/cadastral_number", methods=["POST"])
def cadastral_number():
    cadastral_number = request.form["cadastral_number"]
    return redirect("/result?cadastral_number=" + cadastral_number)


@app.route("/result")
def result():
    cadastral_number = request.args.get("cadastral_number")
    return render_template("result.html", cadastral_number=cadastral_number)


if __name__ == "__main__":
    app.run()
