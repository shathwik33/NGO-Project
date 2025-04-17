from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="mistralai/mistral-small-3.1-24b-instruct:free",
    base_url="https://openrouter.ai/api/v1",
)

prompt = PromptTemplate(
    input_variables=["grade", "subject", "topic", "bloom_verb"],
    template="Create a {bloom_verb} level lesson plan for Grade {grade} about {topic} from {subject}.",
)


def abc(grade, subject, topic, bloom_verb):
    final_prompt = prompt.format(
        grade=grade, subject=subject, topic=topic, bloom_verb=bloom_verb
    )
    return llm.invoke(final_prompt).content
