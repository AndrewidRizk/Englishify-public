import mysql.connector
from googleapiclient.discovery import build
import langdetect
import re

# Replace with your own API key
api_key = ''
youtube = build('youtube', 'v3', developerKey=api_key)

# List of native English-speaking countries
native_english_speaking_countries = ['US', 'GB', 'CA', 'AU', 'NZ', 'IE', 'ZA', 'Unknown']

# Regular expression patterns for non-English scripts
non_english_patterns = {
    'tamil': re.compile(r'[\u0B80-\u0BFF]'),
    'hindi': re.compile(r'[\u0900-\u097F]'),
    # Add more scripts as needed
}

def connect():
    conn = mysql.connector.connect(
        host="74.15.59.128",
        user="Androw_Maged30302",
        password="Androw_Maged30302",
        database="englishify"
    )
    return conn

def get_channel_details(channel_id):
    try:
        request = youtube.channels().list(
            part='snippet',
            id=channel_id
        )
        response = request.execute()
        if not response['items']:
            return 'Unknown', 'Unknown'
        
        channel = response['items'][0]
        country = channel.get('snippet', {}).get('country', 'Unknown')
        description = channel.get('snippet', {}).get('description', '')
        return country, description
    except Exception as e:
        print(f"An error occurred while fetching channel details: {e}")
        return 'Unknown', 'Unknown'

def detect_language(text):
    try:
        detected_language = langdetect.detect(text)
        
        # Manual override for specific non-English scripts
        for lang, pattern in non_english_patterns.items():
            if pattern.search(text):
                return lang
        
        return detected_language
    except Exception:
        return 'unknown'

def is_video_english(video_id):
    
        request = youtube.videos().list(
            part='snippet',
            id=video_id
        )
        response = request.execute()
        
        if not response.get('items', []):
            return False
        
        item = response['items'][0]
        snippet = item['snippet']
        title = snippet.get('title', '')
        description = snippet.get('description', '')
        channel_id = snippet.get('channelId')
        country, channel_description = get_channel_details(channel_id)
        
        title_language = detect_language(title)
        description_language = detect_language(description)
        channel_description_language = detect_language(channel_description)
        
        is_english = (title_language == 'en' and 
                      (description_language == 'en' or description_language == '') and 
                      (channel_description_language == 'en' or channel_description_language == '') and 
                      country in native_english_speaking_countries)
        
        return is_english
    

def fetch_video_ids():
    print("fetching the videos")
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT video_id FROM videos")
    video_ids = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return video_ids

def save_non_english_videos(video_ids):
   
    print("starting to fitch every video")
    non_english_videos = []
    videos_checked = 0
    target = 9472
    current_video = 0
    for video_id in video_ids:
        if current_video > target:
            videos_checked = videos_checked + 1
            try:
                if not is_video_english(video_id):
                    non_english_videos.append(video_id)
            except Exception:
                print("qotas done")
                print(f"number of videos checked are {videos_checked}")
                break
        else:
            current_video = current_video + 1                 
    with open('vids_to_check.txt', 'w') as file:
        for video_id in non_english_videos:
            file.write(f"{video_id}\n")

    return len(non_english_videos)

def main():
    video_ids = fetch_video_ids()
    print(f"count of all videos {len(video_ids)}")
    non_english_count = save_non_english_videos(video_ids)
    print(f"Number of non-English videos: {non_english_count}")

if __name__ == "__main__":
    main()
