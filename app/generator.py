"""
Generation module.

Uses retrieved documents to generate final answer.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import MODEL_NAME, TEMPERATURE


def generate_answer(question: str, documents: list):
    """
    Generates an answer using context from retrieved documents.
    """

    context = "\n\n".join([doc.page_content for doc in documents])

    prompt = ChatPromptTemplate.from_template(
        """
        You are a helpful AI assistant.

        Use the following context to answer the question.
        If the answer is not in the context, say you don't know.

        Context:
        {context}

        Question:
        {question}
        """
    )

    model = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

    chain = prompt | model
    response = chain.invoke({"context": context, "question": question})

    return response.content
