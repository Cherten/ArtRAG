import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
# print("MISTRAL_API_KEY:", os.getenv("MISTRAL_API_KEY"))


class Generator:
    def __init__(self, model="mistral-medium-2505", temperature=0.0):
        self.llm = ChatMistralAI(
            model=model,
            temperature=temperature,
            api_key=os.getenv("MISTRAL_API_KEY")
        )
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Ты эксперт по искусству. Отвечай на вопрос, используя только приведённый контекст. Если ответа нет в контексте, скажи, что не знаешь."),
            ("human", "Контекст:\n{context}\n\nВопрос: {question}")
        ])

    def generate(self, question, context_chunks):
        context = "\n\n".join([c["chunk"]["content"] for c in context_chunks])
        messages = self.prompt.format_messages(context=context, question=question)
        response = self.llm.invoke(messages)
        return response.content