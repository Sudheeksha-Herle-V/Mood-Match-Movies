from pymongo import MongoClient

# MongoDB connection setup
client = MongoClient('mongodb://localhost:27017/')
db = client['MovieDB']
movies_collection = db['movies']

# Define genre pools
positive_genres = ['Action', 'Comedy', 'Drama']
negative_genres = ['Horror', 'Thriller', 'Documentary']

# Map for emotion to sentiment
emotion_dict = {0: 'Angry', 1: 'Disgusted', 2: 'Fearful', 3: 'Happy', 4: 'Neutral', 5: 'Sad', 6: 'Surprised'}

# Function to fetch movies from the database based on genre
def get_movie_from_db(genre):
    try:
        movies = movies_collection.find({"genre": genre})
        movie_names = []
        movie_poster_links = []
        for movie in movies:
            movie_names.append(movie['title'])
            movie_poster_links.append(movie['poster'])
        return movie_names, movie_poster_links
    except Exception as e:
        print(f"Error in get_movie_from_db: {e}")
        return [], []

# Function to suggest movies based on sentiment
def suggest_movie(final_emotion):
    genre_list = get_genres_based_on_sentiment(final_emotion)
    
    movie_names = []
    movie_poster_links = []
    movie_genres = []

    for genre in genre_list:
        movie_name, poster_link = get_movie_from_db(genre)
        movie_names.extend(movie_name)
        movie_poster_links.extend(poster_link)
        movie_genres.extend([genre] * len(movie_name))
    
    return movie_names, movie_poster_links, movie_genres

# Function to get genres based on detected sentiment (emotion)
def get_genres_based_on_sentiment(sentiment_type):
    try:
        if sentiment_type == 'pos': 
            return positive_genres + negative_genres  # Include both positive and negative genres for positive sentiment
        elif sentiment_type == 'neg': 
            return positive_genres  # Only positive genres for negative sentiment
        elif sentiment_type == 'neutral':
            return positive_genres + negative_genres  # Include both positive and negative genres for neutral sentiment
        return []  # Return empty list if sentiment is invalid
    except Exception as e:
        print(f"Error in get_genres_based_on_sentiment: {e}")
        return []

# Function to get the final sentiment based on face emotion
def get_final_sentiment(face_id):
    try:
        emotion = emotion_dict.get(face_id, "neutral")  # Default to neutral if no match
        
        print(f"[DEBUG] Detected emotion: {emotion}")

        if emotion == "Happy" or emotion == "Surprised":
            return 'pos'  # Positive sentiment based on face emotion
        elif emotion == "Angry" or emotion == "Sad" or emotion == "Fearful":
            return 'neg'  # Negative sentiment based on face emotion
        else:
            return 'neutral'  # Neutral sentiment for neutral emotions
    except Exception as e:
        print(f"[ERROR] Error in get_final_sentiment: {e}")
        return 'neutral'  # Default to neutral if there's an error

# Main function to get movie recommendations based on emotion detection and sentiment
def get_all_recom(colors, emotion_id):
    try:
        # Get the final sentiment from emotion detection
        final_sentiment = get_final_sentiment(emotion_id)
        
        # Get genres based on the detected sentiment
        genre_list = get_genres_based_on_sentiment(final_sentiment)
        print(f"[DEBUG] Genres selected for emotion '{final_sentiment}': {genre_list}")
        
        # Fetch movie recommendations based on the selected genres
        movie_names, movie_poster_links, movie_genres = suggest_movie(final_sentiment)
        
        return movie_names, movie_poster_links, movie_genres
    except Exception as e:
        print(f"[ERROR] Error in get_all_recom: {e}")
        return [], [], []
