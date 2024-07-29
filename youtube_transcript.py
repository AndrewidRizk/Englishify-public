'''
implementing the youtube_trancript api
'''

from youtube_transcript_api import YouTubeTranscriptApi

def fetch_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching captions: {e}")
        return None



