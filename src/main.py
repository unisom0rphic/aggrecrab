import streamlit as st
from articleRecommender import ArticleRecommender

def run(request: str):
    """Run recommendations and manage UI state"""
    recommender = ArticleRecommender(request)
    with st.spinner("Finding good articles..."):
        results = recommender.run()
    
    with placeholder.container():
        st.write("Recommendations")
        for i, art in enumerate(results, 1):
            st.write(f"{i}. {art['title']} (Similarity: {art['similarity']})")
            st.write(f"   Reference: {art['url']}")
            st.write()
        
        # FIXME: rendering issues
        # Doesn't reload the page, instead merges both pages (main and results) for a brief moment
        # Could be a streamlit issue, haven't found a good way to prevent this yet
        if st.button("Clear Results"):
            st.session_state.clear()
            st.rerun()

if __name__ == '__main__':
    placeholder = st.empty()
    
    with placeholder.container():
        st.markdown("# Aggrecrab ©")
        req = st.text_input(
            label="Enter your request:", 
            placeholder="Input your request...", 
            max_chars=255,
            key="request"
        )
        if req:
            run(req)
