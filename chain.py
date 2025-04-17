from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
parser = StrOutputParser()

prompt_lesson_plan = PromptTemplate(
    input_variables=["grade", "subject", "topic"],
    template="""
Create a lesson plan for Grade `{grade}` on **{topic}** in **{subject}**, focusing on real-world applications and deeper understanding. Structure your plan exactly as follows, and output only the lesson plan:

(Generate a nice title based on {topic})

1. **Lesson Objective**  
2. **Opening**  
3. **Introduction to New Material**  
4. **Potential Misunderstandings**  
5. **Guided Practice**  
6. **Independent Practice**
7. **Closing**
""",
)

prompt_worksheet = PromptTemplate(
    input_variables=[
        "grade",
        "subject",
        "topic",
        "num_questions",
        "question_format",
        "difficulty",
    ],
    template="""
Worksheet Title: Exploring the {topic}

Instructions:
Answer the following questions based on your understanding of the {topic}. Follow the format: {question_format}.

Section: {question_format}
(Generate {num_questions} questions on {topic}.
- If MCQ: Each must have four options labeled A–D.
- If Short Answer: Each must require 2–3 sentences.
- If Long Answer: Each must require detailed explanations in 5–6 sentences.)

Answer Key:
Provide the correct answer for each question at the end.

Requirements:
- Exactly follow this structure and formatting.
- No extra headings or commentary.
- Difficulty level: {difficulty}.
""",
)

prompt_slides = PromptTemplate(
    input_variables=["grade", "subject", "topic", "num_slides"],
    template="""
Create a {num_slides}-slide presentation for a Grade {grade} {subject} class on the topic: "{topic}". Follow this structure:

- Start with an engaging hook and clear lesson objective.
- Explain why learning {topic} is important and what prior knowledge is needed.
- Introduce main content concepts clearly.
- Include academic vocabulary and common misunderstandings.
- Design a class activity.
- Include independent practice.
- End with a summary and reflection.

Slide Rules:
- Title + 2–4 sentences (simple, clear).
- Match exactly {num_slides} slides.
- No extra text or headings.
- Age-appropriate for Grade {grade}.
""",
)

lesson_plan_chain = prompt_lesson_plan | llm | parser
worksheet_chain = prompt_worksheet | llm | parser
slides_chain = prompt_slides | llm | parser

full_chain = RunnableParallel(
    branches={
        "lesson_plan": lesson_plan_chain,
        "worksheet": worksheet_chain,
        "slides": slides_chain,
    }
)


def invoke(
    grade: str,
    subject: str,
    topic: str,
    num_questions: int,
    question_format: str,
    difficulty: str,
    num_slides: int,
) -> str:
    inputs = {
        "grade": grade,
        "subject": subject,
        "topic": topic,
        "num_questions": num_questions,
        "question_format": question_format,
        "difficulty": difficulty,
        "num_slides": num_slides,
    }
    results = full_chain.invoke(inputs)
    return (
        "***Lesson Plan***\n\n"
        f"{results['branches']['lesson_plan']}\n\n"
        "***Worksheet***\n\n"
        f"{results['branches']['worksheet']}\n\n"
        "***Slides***\n\n"
        f"{results['branches']['slides']}"
    )
