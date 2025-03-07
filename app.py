import streamlit as st
import pickle
import pandas as pd
import requests
from huggingface_hub import hf_hub_download


movies_dict = pickle.load(open("movies_dict.pkl","rb"))  
similarity = pickle.load(open( hf_hub_download(repo_id="sanjayvp/similarity", filename="similarity.pkl"), "rb") )
# similarity = pickle.load(open("similarity.pkl","rb"))

movies = pd.DataFrame(movies_dict)


def fetch_poster(movie_id):
    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d7e3ed7311a954904494cf2cb7f47574&language=en-US")
    data = response.json()
    return f"http://image.tmdb.org/t/p/w500/{data["poster_path"]}"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = similarity[index]
    output = []
    output_posters = []
    # sort based on the second index 
    movies_list =  sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]
    for i in movies_list:
        output_posters.append(fetch_poster(movies.iloc[i[0]].id)) 
        # fetch poster
        output.append(movies.iloc[i[0]].title)
    return output,output_posters

    

st.title("Movie Recommender System")

option = st.selectbox(
    "Select the movie",
    movies['title'].values
)

    
if st.button("Recommend"):
    title, image = recommend(option)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(title[0])
        st.image(image[0])
    with col2:
        st.text(title[1])
        st.image(image[1])
    with col3:
        st.text(title[2])
        st.image(image[2])
    with col4:
        st.text(title[3])
        st.image(image[3])
    with col5:
        st.text(title[4])
        st.image(image[4])


