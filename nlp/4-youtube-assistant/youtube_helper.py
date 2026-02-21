from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

load_dotenv()
embeddings = OpenAIEmbeddings()

def get_transcript_text(video_url: str, languages=['en']) -> str:
    video_id = video_url.split("v=")[-1]
    ytt = YouTubeTranscriptApi()
    transcript_list = ytt.list(video_id)
    transcript = transcript_list.find_transcript(languages)
    fetched = transcript.fetch()
    return " ".join([snippet.text for snippet in fetched])

def create_db_from_youtube_video_url(video_url: str) -> FAISS:

    transcript_text = get_transcript_text(video_url)

    docs = [Document(page_content=transcript_text, metadata={"source": video_url})]

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_docs = text_splitter.split_documents(docs)

    db = FAISS.from_documents(split_docs, embeddings)
    return db

def get_response_from_query(db, query, k=4):

    docs = db.similarity_search(query, k=k)
    docs_page_content = " ".join([d.page_content for d in docs])

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    prompt = ChatPromptTemplate.from_template("""
    You are a helpful assistant that can answer questions about YouTube videos 
    based on the video's transcript.

    Question: {question}
    Transcript: {docs}

    Give a short, concise answer in 1-2 sentences only.
    Only use factual information from the transcript.
    If the transcript doesn't have enough info, say "I don't know".
    """)

    chain = prompt | llm

    result = chain.invoke({"question": query, "docs": docs_page_content})
    return result.content.strip()

if __name__ == "__main__":

    video_url = "https://www.youtube.com/watch?v=Pqb19IaWwOE"
    db = create_db_from_youtube_video_url(video_url)

    query = "What are the main topics discussed in the video?"
    response = get_response_from_query(db, query)

    print(f"Question: {query}")
    print(f"Answer: { response}")