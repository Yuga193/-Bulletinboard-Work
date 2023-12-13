from flask import Flask,render_template, url_for

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("html/main.html")

@app.route("/a")
def build():
    return render_template("html/build.html")

if __name__ == "__main__":
    app.run(debug=True)
