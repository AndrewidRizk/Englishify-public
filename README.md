# **Englishify**

## **Project Overview**
**Englishify** is a web application designed to help second-language learners improve their English skills through real-world video content. By allowing users to search for words or phrases in YouTube captions, Englishify makes it easier to understand how words are used and pronounced in different contexts.

## **Purpose of the Project**
The main goal of Englishify is to provide an interactive and engaging platform for non-native English speakers to:

- **Learn word usage and pronunciation**: Hear words in context, spoken by native speakers in a variety of situations.
- **Improve listening skills**: Experience authentic content instead of static, textbook-based learning.
- **Expand vocabulary**: Discover how specific terms are used in various contexts and understand their nuances.

## **Key Features**
1. **Contextual Word Search**: Users can search for any English word or phrase and see specific instances where the term appears in video captions.
2. **Pronunciation Learning**: The application highlights the searched term in the captions, making it easy to follow along and learn the correct pronunciation.
3. **Dynamic Word Combinations**: For multi-word searches, Englishify generates different combinations and displays additional results, enriching the learning experience.
4. **Search History**: Keeps track of previous searches, allowing users to revisit and reinforce their learning.

## **Technology Stack**
- **Frontend**: React.js for a responsive, user-friendly interface.
- **Backend**: Flask (Python) for handling API requests and text processing.
- **Database**: PostgreSQL for managing search history and storing captions.
- **API**: YouTube Transcript API for retrieving captions and performing text-based searches.

## **Database Overview**
The database is built using **PostgreSQL** and contains three main tables to manage and store data retrieved from YouTube captions. All data was collected using the YouTube API to fetch video metadata and captions.

### **Database Tables**
1. **`youtube_vids`**: Stores basic video metadata such as video ID, title, and URL.
2. **`captions`**: Contains all the caption data for each video, including start time, end time, and the caption text. Each caption is linked to a specific video in the `youtube_vids` table.
3. **`words`**: Stores individual words parsed from the captions along with their position in the sentence. This table is used to speed up word searches and enable partial word queries.

### **Data Collection Process**
- **YouTube API**: The data collection process begins by making calls to the YouTube API to retrieve video details such as title, description, and captions. 
- **Caption Parsing**: Once captions are retrieved, the text is broken down into individual words and phrases. Each word is linked to its position in the `captions` table.
- **Database Population**: The parsed data is stored in the PostgreSQL database under the relevant tables. This structure allows for fast searching and retrieval based on user queries.

### **Database Schema**
The schema is structured to optimize search performance and maintain relationships between videos, captions, and individual words:

- **`youtube_vids`**:
  - `video_id` (Primary Key)
  - `title`
  - `url`

- **`captions`**:
  - `caption_id` (Primary Key)
  - `video_id` (Foreign Key references `youtube_vids`)
  - `start_time`
  - `end_time`
  - `text`

- **`words`**:
  - `word_id` (Primary Key)
  - `caption_id` (Foreign Key references `captions`)
  - `word`
  - `position`

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone https://github.com/username/Englishify.git
cd Englishify

```
### **2. Backend Setup**
Navigate to the backend directory and install dependencies:

```bash
Copy code
pip install -r requirements.txt
```
Set up the PostgreSQL database and start the Flask server:

```bash
Copy code
python main.py
```
### **3. Frontend Setup**
Navigate to the frontend directory and install React dependencies:
```bash
Copy code
cd frontend
npm install
```
Start the React server:

```bash
Copy code
npm start
```
## **License**
This project is licensed under the MIT License. See the LICENSE file for more details.
