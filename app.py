from flask import Flask, request, render_template, render_template_string
from chain import abc
import markdown

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        grade = request.form.get("grade")
        subject = request.form.get("subject")
        topic = request.form.get("topic")
        bloom = request.form.get("bloom")
        md = markdown.markdown(abc(grade, subject, topic, bloom))
        return render_template_string(md)
    return "Submit the form first."


if __name__ == "__main__":
    app.run(debug=True)
