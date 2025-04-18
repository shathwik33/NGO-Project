from flask import Flask, request, render_template, make_response
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
    num_questions = int(request.form.get("num_questions"))
    num_slides = int(request.form.get("num_slides"))
    question_format = request.form.get("question_format")
    subtopics = request.form.get("subtopics")
    difficulty = request.form.get("difficulty")

    try:
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
    except Exception as e:
        html_content = f"<p class='text-red-600'>An error occurred: {e}</p>"

    return render_template("result.html", content=html_content)


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
