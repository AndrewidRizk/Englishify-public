import Database.database as database

# Main function to demonstrate usage
def insert_video_ids_from_file(file_name):
    with open(file_name, 'r') as file:
        video_ids = file.readlines()
        video_ids = [vid.strip() for vid in video_ids]
        count_inserted = 0
        total_video_ids = 0

        for video_id in video_ids:
            # Skip lines starting with '#'
            if not video_id.startswith('#'):
                print("Inserting ", video_id)
                success = database.insert_video(video_id)
                total_video_ids += 1
                if (success == 0):
                    count_inserted += 1
            else:
                print("Header encountered")

    print(f"Successfully inserted {count_inserted} from {total_video_ids} video IDs in {file_name} into the database.")

def main():
    #insert_video_ids_from_file("Data/english_video_ids.txt")    
        

    #words_to_find = ['apple', 'banana' ]
    #matching_videos = database.find_all_words_in_short_videos(words_to_find, max_duration=10)
    #print(f'vid ids: {matching_videos}')
    #for video in matching_videos:
    #    print(f"Video ID: {video['video_id']}")
    #    for word, occurrences in video['word_occurrences'].items():
    #        print(f"  Word: {word}")
    #        for occurrence in occurrences:
    #            print(f"    Start Time: {occurrence['start_time']}, End Time: {occurrence['end_time']}")     
    
    #Search for phrase in MySQL
    results = database.search_phrase(["videos", "about"])
    for result in results:
        print(result)
    print(len(results))


    
if __name__ == "__main__":
    main()