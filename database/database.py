import mysql.connector
import youtube_transcript
import postgre
import elasticsearchDB
import redisDB


def connect():
    # Global variable for database connection
    conn = mysql.connector.connect(
        host="",
        user="",
        password="",
        database=""
    )
    
    return conn

def video_exists(video_id):
    conn = connect()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM Videos WHERE video_id = %s"
    cursor.execute(query, (video_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] > 0

def insert_video(video_id):
    # Check if the video already exists in the database
    if video_exists(video_id):
        print(f"Video with ID {video_id} already exists in the database. Skipping insertion.")
        return -1
    
    # Fetch captions from YouTube
    captions = youtube_transcript.fetch_captions(video_id)
    try:
        if captions:
            video_data = {
                'video_id': video_id,
                'title': 'Example Title',
                'url': f'https://www.youtube.com/watch?v={video_id}'
            }
            
            # Insert video metadata into MySQL
            insert_video_metadata(video_data)
            
            # Insert captions and word index into MySQL
            insert_captions_and_word_index(video_id, captions)

            print("Insertion Success")
            return 0
        else:
            print("Insertion Failed: No captions")
            return -1
    except Exception as e:
        print(f"Failed to insert video {video_id}: {e}")
        return -1


# Function to insert video metadata into MySQL
def insert_video_metadata(video_data):
    conn = connect()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO Videos (video_id, title, url)
    VALUES (%s, %s, %s)
    ON DUPLICATE KEY UPDATE video_id=video_id;
    """
    cursor.execute(query, (video_data['video_id'], video_data['title'], video_data['url']))
    conn.commit()
    cursor.close()
    conn.close()
    

# Function to insert captions and word index into MySQL
def insert_captions_and_word_index(video_id, captions):
    conn = connect()
    cursor = conn.cursor()
    
    caption_query = """
    INSERT INTO Captions (video_id, start_time, end_time, text)
    VALUES (%s, %s, %s, %s)
    """
    
    word_index_query = """
    INSERT INTO Word_index (word, caption_id, position, video_id)
    VALUES (%s, %s, %s, %s)
    """
    
    for caption in captions:
        cursor.execute(caption_query, (video_id, int(caption['start']), int(caption['start'] + caption['duration']), caption['text']))
        caption_id = cursor.lastrowid
        
        words = caption['text'].split()
        for position, word in enumerate(words):
            cursor.execute(word_index_query, (word.lower(), caption_id, position, video_id))
    
    conn.commit()
    cursor.close()
    conn.close()

# Function to search for phrases in MySQL
def search_phrase(words):
    conn = connect()
    cursor = conn.cursor()

    try:
        if len(words) == 1:
            query = """
            SELECT c.caption_id, c.video_id, c.start_time, c.end_time, c.text
            FROM Captions c
            JOIN Word_index w ON c.caption_id = w.caption_id
            WHERE w.word = %s
            ORDER BY c.start_time;
            """
            cursor.execute(query, (words[0],))

        elif len(words) > 1:
            placeholders = ', '.join(['%s'] * len(words))
            query = f"""
                SELECT c.caption_id, c.video_id, c.start_time, c.end_time, c.text
                FROM Captions c
                JOIN (
                    SELECT caption_id, video_id
                    FROM Word_index
                    WHERE word IN ({placeholders})
                    GROUP BY caption_id, video_id
                    HAVING COUNT(DISTINCT word) = %s
                ) i ON c.caption_id = i.caption_id
                WHERE {' AND '.join([f'EXISTS (SELECT 1 FROM Word_index idx{j} WHERE idx{j}.caption_id = c.caption_id AND idx{j}.word = %s)' for j in range(len(words))])}
                ORDER BY c.start_time;
                """
                
            # Prepare the parameters
            params = []
            params.extend(words)  # For word IN (%s, %s, ...)
            params.append(len(words))  # For COUNT(DISTINCT word) = %s
            params.extend(words)  # For EXISTS (SELECT 1 ... WHERE idx.word = %s)

            cursor.execute(query, tuple(params))

        else:
            return []

        # Fetch all results
        results = cursor.fetchall()

        return results

    finally:
        cursor.close()
        conn.close()


def read_video_ids(file_path):
    with open(file_path, 'r') as file:
        video_ids = [line.strip() for line in file.readlines()]
    return video_ids

def get_total_videos():
    db_connection = connect()
    cursor = db_connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM videos")
    total_videos = cursor.fetchone()[0]
    cursor.close()
    db_connection.close()
    return total_videos
    

def delete_videos_and_related_data(video_ids):
    deleted_count = 0
    print("delete started...")
    for video_id in video_ids:
        db_connection = connect()
        cursor = db_connection.cursor()
        cursor.execute("DELETE FROM word_index WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM captions WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM videos WHERE video_id = %s", (video_id,))
        db_connection.commit()
        affected_rows = cursor.rowcount
        if affected_rows > 0:
            deleted_count += 1
        cursor.close()
        db_connection.close()
    return deleted_count