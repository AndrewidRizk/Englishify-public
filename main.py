import database.database as database

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
    #insert_video_ids_from_file("video_ids.txt")    
        
    #Search for phrase in MySQL
    #results = database.search_phrase(["Andrew"])
    #for result in results:
    #    print(result)
    file_path = './Data/vids_to_check.txt'
    video_ids = database.read_video_ids(file_path)
    print("Getting a list of the files")
    
    total_videos_before = database.get_total_videos()
    print(f"Total videos before deletion: {total_videos_before}")
    deleted_videos_count = database.delete_videos_and_related_data(video_ids)
    total_videos_after = database.get_total_videos()
    
    print(f"Total videos after deletion: {total_videos_after}")
    print(f"Total videos deleted: {deleted_videos_count}")



    #print(len(results))
    
if __name__ == "__main__":
    main()