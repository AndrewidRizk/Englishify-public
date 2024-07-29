from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import database.database as database  # Make sure to import your database module

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_videos():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    words = query.split()
    results = database.search_phrase(words)
    
    # Process results to the desired format
    videos = []
    video_dict = {}
    for result in results:
        video_id = result[1]
        caption = {'start_time': result[2], 'end_time': result[3], 'text': result[4]}
        if video_id not in video_dict:
            video_dict[video_id] = {
                'video_id': video_id,
                'title': result[4],  # Assuming 'text' contains the title or some relevant information
                'captions': []
            }
        video_dict[video_id]['captions'].append(caption)
    
    videos = list(video_dict.values())
    return jsonify({'videos': videos})

if __name__ == '__main__':
    app.run(debug=True)
