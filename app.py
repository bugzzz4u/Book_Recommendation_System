import pickle
import streamlit as st
import numpy as np

#Loading the necessary embeddings
st.header("Book Recommender System using Machine Learning")
model = pickle.load(open('artifacts/model.pkl','rb'))
books_name = pickle.load(open('artifacts/books_name.pkl','rb'))
final_rating = pickle.load(open('artifacts/final_rating.pkl','rb'))
book_pivot = pickle.load(open('artifacts/book_pivot.pkl','rb'))

def fetch_poster(suggestions):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestions:
        book_name.append(book_pivot.index[book_id])
    
    #Identify the book and then its index and then it will append the indices
    for name in book_name[0]:
        ids = np.where(final_rating['title'] == name)[0][0]
        ids_index.append(ids)
    
    #Fetching poster by id
    for idx in ids_index:
        url = final_rating.iloc[idx]['image_url']
        poster_url.append(url)
    return poster_url


def recommend_books(book_name):
    book_list = []
    book_id = np.where(book_pivot.index == book_name)[0][0]
    distances, suggestions = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors = 6)
    
    poster_url = fetch_poster(suggestions)

    for i in range(len(suggestions)):
        books = book_pivot.index[suggestions[i]]
        for j in books:
            book_list.append(j)
    return book_list, poster_url

selected_books = st.selectbox(
    "Type or Select a book",
    books_name
)

if st.button('Show recommendations'):
    recommended_books, poster_url = recommend_books(selected_books)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommended_books[1])
        st.image(poster_url[1])

    with col2:
        st.text(recommended_books[2])
        st.image(poster_url[2])

    with col3:
        st.text(recommended_books[3])
        st.image(poster_url[3])
    
    with col4:
        st.text(recommended_books[4])
        st.image(poster_url[4])
    
    with col5:
        st.text(recommended_books[5])
        st.image(poster_url[5])