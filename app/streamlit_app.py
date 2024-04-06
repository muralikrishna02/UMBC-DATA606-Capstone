import streamlit as st
import pandas as pd
from imdb import IMDb
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors

# Cached IMDb object
m_obj = IMDb()

#for getting the movie poster
def get_movie_poster(title):
    movie = m_obj.search_movie(title)
    if movie:
        movie = m_obj.get_movie(movie[0].movieID)
        return movie.get('cover url')
    else:
        return None
# displaying the movie posters 
def display_movies(movie_titles, ncols=3):
    nrows = -(-len(movie_titles) // ncols) 
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 5*nrows)) 
    
    # to check the progress updates
    progress_text = st.empty()
    # using spinner to show the loading icon
    with st.spinner("Loading movie posters..."): 
        for i, title in enumerate(movie_titles):
            poster_url = get_movie_poster(title)
            if poster_url:
                response = requests.get(poster_url)
                img = Image.open(BytesIO(response.content))
                ax = axes[i // ncols, i % ncols]
                ax.imshow(img)
                ax.set_title(title, fontsize=10, pad=5)  
                ax.axis('off')
            else:
                axes[i // ncols, i % ncols].axis('off')
                axes[i // ncols, i % ncols].set_title("Poster not available", fontsize=10, pad=5)
            
            # Updating the progress 
            progress_text.text(f"Loading poster {i + 1} of {len(movie_titles)}")

        # Hiding the empty subplots
        for j in range(i + 1, len(movie_titles)):
            axes[j // ncols, j % ncols].axis('off')

        plt.tight_layout()
        st.pyplot(fig)

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('movie_data.csv')

# Content-Based Filtering
def content_based_recommendations(mv_title, mv_data, rec_n=6):

    # performing tf-idf vectorization and calculating the cosine similarity
    # providinng recommendations
    cb_tfv = TfidfVectorizer()
    matrix_cb_tf = cb_tfv.fit_transform(mv_data['combined_text'])
    
    sim_co = cosine_similarity(matrix_cb_tf, matrix_cb_tf)
    
    mv_ind = mv_data[mv_data['title'].str.lower() == mv_title.lower()].index[0]
    
    ip_mv_scores = list(enumerate(sim_co[mv_ind]))

    ip_mv_scores = sorted(ip_mv_scores, key=lambda x: x[1], reverse=True)
    
    # recommended movies
    recom_list = ip_mv_scores[1:rec_n+1]
    mov_top = [i[0] for i in recom_list]
    
    return mv_data.iloc[mov_top]['title'].tolist()


# Collaborative Filtering
def collaborative_filtering_recommendations(mv_name, mv_df, near_neigh=10, rec_n=6):
    # selecting numeric colums for the model ,nearest neighor algo
    mv_df_num = mv_df.select_dtypes(include='number')
    near_neigh_mdl = NearestNeighbors(n_neighbors=near_neigh, metric='cosine')
    near_neigh_mdl.fit(mv_df_num)
    # getting index to fing nearest neighbours
    title_index = mv_df[mv_df['title'].str.lower() == mv_name.lower()].index[0]
    
    # getting dist and indx
    kn_dist, kn_ind = near_neigh_mdl.kneighbors([mv_df_num.iloc[title_index]])
    
    neigh_indices = kn_ind.flatten()[1:]
    # to show recommendations
    recomm_titles = mv_df.iloc[neigh_indices]['title'].tolist()[:rec_n]
    return recomm_titles

# Combined Approach
def combined_recommendations(title, mv_d, weight=0.5, rec_n=3):
    # getting both content based and collabarative 
    content_based_op = content_based_recommendations(title, mv_d, rec_n)
    collaborative_op = collaborative_filtering_recommendations(title, mv_d, near_neigh=10, rec_n=rec_n)
    # combining the ouputs 
    combined_results = list(set(content_based_op) | set(collaborative_op))
    return combined_results


# Streamlit app layout and user interaction
st.title('Movie Recommendation System')

# Load data
data = load_data()

# User input for movie title
movie_title = st.selectbox("Select a movie title:", data['title'])

# Recommendation method selection using a dropdown menu
selected_method = st.selectbox("Select recommendation method:", ["Content-Based", "Collaborative Filtering", "Combined"])

# Get recommendations based on selected method
if st.button('Get Recommendations'):
    if selected_method == "Content-Based":
        recommendations = content_based_recommendations(movie_title, data)
    elif selected_method == "Collaborative Filtering":
        recommendations = collaborative_filtering_recommendations(movie_title, data)
    else:  # Combined recommendations
        recommendations = combined_recommendations(movie_title, data)

    # Display recommendations
    st.title("Recommended Movies")
    st.write("Here are some movies you might like:")
    for recommendation in recommendations:
        st.write(f"- {recommendation}")

    # Display posters for recommended movies
    st.title("Movie Posters")
    st.write("Fetching and displaying movie posters for recommended movies...")
    display_movies(recommendations)
