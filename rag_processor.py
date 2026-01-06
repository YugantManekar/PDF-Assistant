from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAGProcessor:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", temperature=0.3
        )

        self.prompt = ChatPromptTemplate.from_template("""
Answer ONLY from context. If unknown, say you don't know.

Context:
{context}

Question:
{question}
""")

    def create_chain(self, retriever):
        return (
            {"context": retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def translate(self, text, language):
        return self.llm.invoke(f"Translate to {language}:\n{text}")
