from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

def get_transcript_text(video_url: str, languages=['en']) -> str:
    video_id = video_url.split("v=")[-1]
    ytt = YouTubeTranscriptApi()
    transcript_list = ytt.list(video_id)
    transcript = transcript_list.find_transcript(languages)
    fetched = transcript.fetch()
    return " ".join([snippet.text for snippet in fetched])

video_url = "https://www.youtube.com/watch?v=Pqb19IaWwOE"
print(get_transcript_text(video_url))