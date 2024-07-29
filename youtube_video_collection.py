import googleapiclient.discovery
import time
from Data.englishCheck import is_video_english

def get_youtube_service():
    api_service_name = "youtube"
    api_version = "v3"
    api_key = ""
    return googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)


def fetch_english_video_ids(youtube, queries, max_results, fetched_ids):
    video_ids = []
    for query in queries:
        request = youtube.search().list(
            part="id",
            q=query,
            type="video",
            maxResults=max_results,
            relevanceLanguage="en",
            videoCaption="closedCaption",
            regionCode="CA",
            videoDefinition="high"
        )
        response = request.execute()
        for item in response.get('items', []):
            video_id = item['id']['videoId']
            if video_id not in fetched_ids:
                fetched_ids.add(video_id)
                video_ids.append(video_id)
    return video_ids

def write_video_ids_to_file(video_ids, filename):
    with open(filename, 'a') as file:  # Changed 'w' to 'a' to append to the file
        for video_id in video_ids:
            file.write(f"{video_id}\n")

def main():
    youtube = get_youtube_service()
    queries = ["india"]
    max_results = 10
    total_fetched = 0
    quota_limit = 100
    quota_per_request = 100
    fetched_ids = set()
    english_video_ids = []
    non_english_video_ids = []

    while total_fetched < (quota_limit // quota_per_request) * max_results:
        video_ids = fetch_english_video_ids(youtube, queries, max_results, fetched_ids)

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

    # Write English video IDs to file
    write_video_ids_to_file(english_video_ids, "english_video_ids.txt")
    print(f"Fetched and wrote {len(english_video_ids)} English video IDs. Total fetched: {total_fetched}")

    # Write non-English video IDs to file
    write_video_ids_to_file(non_english_video_ids, "non_english_video_ids.txt")
    print(f"Fetched and wrote {len(non_english_video_ids)} non english video IDs. Total fetched: {total_fetched}")

if __name__ == "__main__":
    main()
