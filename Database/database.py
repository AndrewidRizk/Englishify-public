import psycopg2
from psycopg2 import sql
from . import youtube_transcript as youtube_transcript
from . import db_connection 

def video_exists(video_id):
    conn = db_connection.connect_postgresql()
    cursor = conn.cursor()
    query = "SELECT COUNT(*) FROM Videos WHERE video_id = %s"
    cursor.execute(query, (video_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] > 0

def insert_video(video_id):
    if video_exists(video_id):
        print(f"Video with ID {video_id} already exists in the database. Skipping insertion.")
        return -1
    
    captions = youtube_transcript.fetch_captions(video_id)
    try:
        if captions:
            video_data = {
                'video_id': video_id,
            }
            
            insert_video_metadata(video_data)
            insert_captions_and_word_index(video_id, captions)

            print("Insertion Success")
            return 0
        else:
            print("Insertion Failed: No captions")
            return -1
    except Exception as e:
        print(f"Failed to insert video {video_id}: {e}")
        return -1
    
def insert_video_metadata(video_data):
    conn = db_connection.connect_postgresql()
    cursor = conn.cursor()

    query = """
    INSERT INTO Videos (video_id)
    VALUES (%s)
    ON CONFLICT (video_id) DO NOTHING;
    """
    cursor.execute(query, (video_data['video_id'],))
    conn.commit()
    cursor.close()
    conn.close()
    

def insert_captions_and_word_index(video_id, captions):
    conn = db_connection.connect_postgresql()
    cursor = conn.cursor()
    
    caption_query = """
    INSERT INTO Captions (video_id, start_time, end_time, text)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (video_id, start_time) DO NOTHING
    RETURNING caption_id
    """
    
    word_index_query = """
    INSERT INTO Word_index (word, caption_id, position, video_id)
    VALUES (%s, %s, %s, %s)
    """
    
    for caption in captions:
        cursor.execute(caption_query, (video_id, int(caption['start']), int(caption['start'] + caption['duration']), caption['text']))
        caption_id = cursor.fetchone()
        
        if caption_id is None:
            # Caption already exists; skip word insertion for this caption
            continue
        
        caption_id = caption_id[0]
        words = caption['text'].split()
        for position, word in enumerate(words):
            cleaned_word = ''.join(filter(str.isalnum, word)).lower()  # Remove punctuation, make lowercase
            cursor.execute(word_index_query, (cleaned_word, caption_id, position, video_id))
    
    conn.commit()
    cursor.close()
    conn.close()



def search_phrase(words):
    conn = db_connection.connect_postgresql()
    cursor = conn.cursor()

    normalized_words = [normalize_word(word) for word in words]

    try:
        if len(words) == 1:
            query = """
            SELECT c.caption_id, c.video_id, c.start_time, c.end_time, c.text
            FROM Captions c
            JOIN Word_index w ON c.caption_id = w.caption_id
            WHERE w.word = %s
            ORDER BY c.start_time;
            """
            cursor.execute(query, (normalized_words[0],))

        elif len(words) > 1:
            placeholders = ', '.join(['%s'] * len(normalized_words))
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
                
            params = []
            params.extend(normalized_words)
            params.append(len(normalized_words))
            params.extend(normalized_words)

            cursor.execute(query, tuple(params))

        else:
            return []

        results = cursor.fetchall()
        return results

    finally:
        cursor.close()
        conn.close()

def normalize_word(word):
    return ''.join(filter(str.isalnum, word)).lower()


def read_video_ids(file_path):
    with open(file_path, 'r') as file:
        video_ids = [line.strip() for line in file.readlines()]
    return video_ids

def get_total_videos():
    conn = db_connection.connect_postgresql()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Videos")
    total_videos = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total_videos

def delete_videos_and_related_data(video_ids):
    deleted_count = 0
    print("delete started...")
    for video_id in video_ids:
        conn = db_connection.connect_postgresql()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Word_index WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM Captions WHERE video_id = %s", (video_id,))
        cursor.execute("DELETE FROM Videos WHERE video_id = %s", (video_id,))
        conn.commit()
        affected_rows = cursor.rowcount
        if affected_rows > 0:
            deleted_count += 1
        cursor.close()
        conn.close()
    return deleted_count


from pytube import YouTube

def get_video_length(video_id):
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        return yt.length / 60  # Convert seconds to minutes
    except Exception as e:
        print(f"Error fetching video length for {video_id}: {e}")
        return None

def find_all_words_in_short_videos(words, max_duration=10):
    conn = db_connection.connect_postgresql()
    cursor = conn.cursor()

    normalized_words = [normalize_word(word) for word in words]

    if not normalized_words:
        return []

    placeholders = ', '.join(['%s'] * len(normalized_words))
    query = f"""
    SELECT video_id
    FROM Word_index
    WHERE word IN ({placeholders})
    GROUP BY video_id
    HAVING COUNT(DISTINCT word) = %s;
    """

    try:
        cursor.execute(query, tuple(normalized_words + [len(normalized_words)]))
        all_videos = cursor.fetchall()

        results = []
        for video_id in all_videos:
            duration = get_video_length(video_id[0])
            if duration is not None and duration <= max_duration:
                word_occurrences = {}
                for word in normalized_words:
                    cursor.execute("""
                    SELECT c.video_id, w.word, c.start_time, c.end_time
                    FROM Word_index w
                    JOIN Captions c ON w.caption_id = c.caption_id
                    WHERE w.video_id = %s AND w.word = %s
                    ORDER BY c.start_time;
                    """, (video_id[0], word))

                    occurrences = cursor.fetchall()
                    if word not in word_occurrences:
                        word_occurrences[word] = []

                    for occurrence in occurrences:
                        word_occurrences[word].append({
                            'video_id': occurrence[0],
                            'word': occurrence[1],
                            'start_time': occurrence[2],
                            'end_time': occurrence[3]
                        })

                results.append({
                    'video_id': video_id[0],
                    'word_occurrences': word_occurrences
                })

        return results
    finally:
        cursor.close()
        conn.close()
