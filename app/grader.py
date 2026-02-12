"""
Relevance grader.

Checks if retrieved documents are relevant to the question.
Used for conditional routing.
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.config import MODEL_NAME


def grade_relevance(question: str, documents: list) -> bool:
    """
    Returns True if documents are relevant.
    """

    context = "\n".join([doc.page_content for doc in documents])

    prompt = ChatPromptTemplate.from_template(
        """
        Determine if the retrieved context is relevant
        to answer the question.

        Question:
        {question}

        Context:
        {context}

        Answer only 'yes' or 'no'.
        """
    )

    model = ChatOpenAI(model=MODEL_NAME, temperature=0)

    chain = prompt | model
    response = chain.invoke({"question": question, "context": context})

    return "yes" in response.content.lower()
