from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from transformers import pipeline
from langchain_community.llms import HuggingFacePipeline

loader = TextLoader("book.txt", encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(texts, embedding_model)

local_pipe = pipeline(
    "text-generation",
    model="./fine_tuned_neo",
    tokenizer="./fine_tuned_neo",
    max_new_tokens=120,
    do_sample=True,
    temperature=0.7,
    pad_token_id=50256,
    eos_token_id=50256,
)

llm = HuggingFacePipeline(pipeline=local_pipe)

# Correct prompt template using variables 'question' and 'context'
template = """
Use the following context to answer the question concisely.
If you don't know the answer, say so.

Context:
{context}

Question:
{question}

Answer:"""

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=template,
)

qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt},  # pass prompt here for combining docs
)

def answer_question(query: str) -> str:
    return qa.run(query)

if __name__ == "__main__":
    print("Type 'exit' to quit.")
    while True:
        q = input("Question: ")
        if q.lower() == "exit":
            break
        print("Answer:", answer_question(q))
