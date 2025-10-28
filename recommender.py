import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    try:
        response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
        response_data = response.json()
        if 'poster_path' in response_data and response_data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + response_data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_distances = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_distances:
        # Get the actual movie_id from the dataframe, not the index
        movie_id = movies_df.iloc[i[0]].movie_id
        
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

movies_df = pickle.load(open('movies.pkl','rb'))
movies_list = movies_df['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender System")
st.write("Welcome to the Movie Recommender System! Here you can find movie recommendations based on your preferences.")

selected_movie_name = st.selectbox(
    'Select a movie you like:',
    movies_list)

if st.button('Show Recommendation'):
    recommended_movies, recommended_posters = recommend(selected_movie_name)
    
    # Display recommendations in columns
    cols = st.columns(5)
    for idx, (movie, poster) in enumerate(zip(recommended_movies, recommended_posters)):
        with cols[idx]:
            st.text(movie)
            st.image(poster)


