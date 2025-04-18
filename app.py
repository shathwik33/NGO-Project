from flask import Flask, request, render_template
from chain import invoke
import markdown2
import os

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/result", methods=["POST"])
def result():
    grade = request.form.get("grade")
    subject = request.form.get("subject")
    topic = request.form.get("topic")
    num_questions = request.form.get("num_questions")
    num_slides = request.form.get("num_slides")
    question_format = request.form.get("question_format")
    subtopics = request.form.get("subtopics")
    difficulty = request.form.get("difficulty")

    response_text = invoke(
        grade=grade,
        subject=subject,
        topic=topic,
        subtopics=subtopics,
        num_questions=num_questions,
        question_format=question_format,
        difficulty=difficulty,
        num_slides=num_slides,
    )

    html_content = markdown2.markdown(response_text)

    return render_template("result.html", content=html_content)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
