from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

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

video_url = "https://www.youtube.com/watch?v=Pqb19IaWwOE"
db = create_db_from_youtube_video_url(video_url)
print(db)