import streamlit as st
from articleRecommender import ArticleRecommender

def run():
    recommender = ArticleRecommender("config.yaml")
    results = recommender.run()
    
    st.write("Recommendations")
    for i, art in enumerate(results, 1):
        st.write(f"{i}. {art['title']} (Similarity: {art['similarity']})")
        st.write(f"   Reference: {art['url']}")
        st.write()


st.title("Aggrecrab ©")
st.button('RUN', on_click=run)
    