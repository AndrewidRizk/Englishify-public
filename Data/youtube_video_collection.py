import googleapiclient.discovery
import time
from englishCheck import is_video_english

def get_youtube_service():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = ""  # Replace with your actual API key
    return googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

def fetch_english_video_ids(youtube, queries, max_results, fetched_ids):
    video_ids = []
    for query in queries:
        next_page_token = None
        while True:
            request = youtube.search().list(
                part="id",
                q=query,
                type="video",
                maxResults=min(max_results, 50),  # maxResults capped at 50
                relevanceLanguage="en",
                videoCaption="closedCaption",
                regionCode="CA",
                videoDefinition="high",
                pageToken=next_page_token  # Handle pagination
            )
            response = request.execute()
            for item in response.get('items', []):
                video_id = item['id']['videoId']
                if video_id not in fetched_ids:
                    fetched_ids.add(video_id)
                    video_ids.append(video_id)
            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(video_ids) >= max_results:
                break
    return video_ids

def write_video_ids_to_file(video_ids, filename):
    with open(filename, 'a') as file:
        for video_id in video_ids:
            file.write(f"{video_id}\n")

def main():
    youtube = get_youtube_service()
    queries = ["watchmojo movies 2024", "watchmojo movies 2022"]
    max_results = 1000
    total_fetched = 0
    quota_limit = 8000
    quota_per_request = 1
    fetched_ids = set()
    english_video_ids = []
    non_english_video_ids = []

    try:
        while total_fetched < (quota_limit // quota_per_request) * max_results:
            video_ids = fetch_english_video_ids(youtube, queries, max_results - total_fetched, fetched_ids)

            for video_id in video_ids:
                if is_video_english(video_id):
                    english_video_ids.append(video_id)
                else:
                    non_english_video_ids.append(video_id)
                    print(f"Non-English video removed: {video_id}")

            total_fetched += len(video_ids)
            print(f"Fetched and checked {len(video_ids)} video IDs. Total fetched: {total_fetched}")

            if len(video_ids) == 0:
                break

            time.sleep(1)  # Avoid hitting rate limits
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Write English video IDs to file
        write_video_ids_to_file(english_video_ids, "Data/english_video_ids.txt")
        print(f"Fetched and wrote {len(english_video_ids)} English video IDs.")

        # Write non-English video IDs to file
        write_video_ids_to_file(non_english_video_ids, "Data/non_english_video_ids.txt")
        print(f"Fetched and wrote {len(non_english_video_ids)} non-English video IDs.")

if __name__ == "__main__":
    main()
