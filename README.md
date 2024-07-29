# Englishify-public

- This is a public version of my private repositary.
- The project still is not ready yet
- I had to make a data clean up, deciding that i need to change my database from SQL to Postgre and elastic search

# 1. Concept

    Define Objectives:
        - Create a webapp where users can search for specific word, and results of youtube videos, podcasts and audiobooks with the given word
          is provided. The given content is played at the time where the word is said.
        - This project is inspired by https://youglish.com/, which does the same thing with youtube videos, but tweeking a bit adding the meaning of the videos and all deferent versons and verbs or it and there videos.

    Target Audience:
        - Language learners and educators. This will help students hear a given word being pronounced and used by native
          speakers in a practical context, making it a useful resource for educators too.

    Features:
        - Search Functionality: Allow users to search for content based on keywords.
        - Playback: Stream all the content that is found directly, at the given time where the keywords are used.
        - Responsive Design: Ensure the website works well across various devices and screen sizes.
# 2. Technical Requirements
Data Collection:

    Collecting video IDs, captions, and storing them in a PostgreSQL database.
    Ensure accurate timestamping of when specific words are spoken.
    Frontend:
    
    Technologies: React.js for building dynamic user interfaces.
    Styling: Tailwind CSS for responsive and modern design.
    Integration: Utilize Axios for communicating with the backend APIs.
    Backend:
    
    Framework: Python with Flask to develop RESTful APIs for connecting the database to the frontend.
    Deployment:
    
    Hosting: Deploy the frontend and backend on Vercel for seamless integration and scalability.
# 3. Architecture Design
    Frontend Components:
    
    Search Component: Allows users to input queries and sends requests to the backend.
    Result Display: Shows search results with video details and playback options.
    Player Component: Facilitates video playback with precise timing of captions.
    Dynamic Text Component: Displays captions with highlighted searched words.
    Filters: Options to select content type (e.g., podcasts, songs, audiobooks), age, and level.
    Backend Structure:
    
    API Endpoints:
    /search
    /play
    /captions
    ...
    Controllers: Manage business logic for processing search queries, handling user sessions, and interacting with external APIs (e.g., YouTube Data API).
