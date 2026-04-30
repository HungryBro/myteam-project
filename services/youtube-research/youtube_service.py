import os
import json
import datetime
from typing import List, Dict, Optional
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from openai import OpenAI
import httpx
from dotenv import load_dotenv

load_dotenv()

# Configuration
VAULT_PATH = os.getenv("VAULT_PATH", "../../km-vault/research/youtube-summaries/")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def get_latest_videos(channel_url: str, limit: int = 5) -> List[Dict]:
    """Fetch latest videos from a channel using yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"{channel_url}/videos", download=False)
            videos = []
            if 'entries' in info:
                for entry in info['entries'][:limit]:
                    videos.append({
                        'id': entry['id'],
                        'title': entry['title'],
                        'url': f"https://www.youtube.com/watch?v={entry['id']}",
                        'upload_date': entry.get('upload_date') # YYYYMMDD
                    })
            return videos
        except Exception as e:
            print(f"Error fetching videos for {channel_url}: {e}")
            return []

def get_transcript(video_id: str) -> Optional[str]:
    """Fetch transcript for a given video ID."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['th', 'en'])
        return " ".join([t['text'] for t in transcript_list])
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None

def summarize_with_ai(transcript: str, video_url: str) -> Dict:
    """Summarize transcript using OpenRouter API."""
    prompt = f"""
    Analyze the following YouTube video transcript and provide a trading summary.
    Transcript: {transcript[:10000]} # Limit transcript length
    
    Format the output as a JSON object with the following keys:
    - signal: "BUY", "SELL", or "HOLD"
    - symbol: The currency pair or asset mentioned (e.g., "BTCUSDT", "XAUUSD")
    - reasoning: A brief explanation of the reasoning
    - timeframe: The timeframe mentioned (e.g., "1h", "4h", "Daily")
    - confidence_score: Initial confidence (0-5)
    
    If no clear signal is found, use "HOLD" and explain why.
    """
    
    try:
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional financial analyst assistant."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        summary = json.loads(response.choices[0].message.content)
        summary['video_url'] = video_url
        summary['timestamp'] = datetime.datetime.now().isoformat()
        return summary
    except Exception as e:
        print(f"Error summarizing with AI: {e}")
        return {
            "signal": "ERROR",
            "symbol": "UNKNOWN",
            "reasoning": str(e),
            "timeframe": "UNKNOWN",
            "video_url": video_url,
            "timestamp": datetime.datetime.now().isoformat()
        }

def save_to_vault(summary: Dict, video_id: str):
    """Save the summary to the KM Vault."""
    os.makedirs(VAULT_PATH, exist_ok=True)
    filename = f"{datetime.datetime.now().strftime('%Y%m%d')}_{video_id}.json"
    filepath = os.path.join(VAULT_PATH, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Saved summary to {filepath}")

def run_research():
    """Main execution flow for YouTube research."""
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    for channel in config['channels']:
        print(f"Processing channel: {channel['name']}")
        videos = get_latest_videos(channel['url'])
        
        # Filter videos from the last 24 hours
        today = datetime.datetime.now().strftime('%Y%m%d')
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        
        for video in videos:
            if video['upload_date'] in [today, yesterday]:
                print(f"Analyzing video: {video['title']}")
                transcript = get_transcript(video['id'])
                if transcript:
                    summary = summarize_with_ai(transcript, video['url'])
                    save_to_vault(summary, video['id'])
                else:
                    print(f"No transcript available for {video['id']}")

if __name__ == "__main__":
    run_research()
