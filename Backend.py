from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development only; restrict in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    video_url: str

@app.post('/download')
def download_youtube_video(request: VideoRequest):
    video_url = request.video_url
    ydl_opts = {
        'format': 'best',  # Best video quality
        'outtmpl': '%(title)s.%(ext)s',  # Save file as video title
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        return {"message": "Video downloaded successfully!"}
    except Exception as e:
        return {"error": str(e)}
