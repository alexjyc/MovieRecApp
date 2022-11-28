import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '45c36246bc4deb46851f353b8f000887'

movie_clf = pickle.load(open('movie_clf.pkl', 'rb'))
cos_sim = pickle.load(open('cos_sim.pkl', 'rb'))

def getRecommends(title):
    idx = movie_clf[movie_clf['title'] == title].index[0]

    cos_val = sorted(enumerate(cos_sim[idx]), key=lambda x: x[1], reverse=True)

    movie_idx = [i[0] for i in cos_val[1: 11]]

    image, title = [], []
    for j in movie_idx:
        id = movie_clf['id'].iloc[j]
        detail = movie.details(id)
        image_path = detail['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpeg'
        image.append(image_path)
        title.append(detail['title'])
    
    return image, title


st.set_page_config(layout='wide')
st.header("Alex's Choice")

movie_list = movie_clf['title'].values
title = st.selectbox("What type of movie do you want to watch tonight?", movie_list)

if st.button('Recommend'):
    with st.spinner('Showtime!'):
        images, titles = getRecommends(title)

        idx = 0
        for x in range(2):
            col = st.columns(5)
            for c in col:
                c.image(images[idx])
                c.write(titles[idx])
                idx += 1
