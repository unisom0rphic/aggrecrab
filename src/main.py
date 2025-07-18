import streamlit as st
from articleRecommender import ArticleRecommender

def run():
    """Run recommendations and manage UI state."""
    recommender = ArticleRecommender("config.yaml")
    with st.spinner("Finding good articles..."):
        results = recommender.run()
    
    with placeholder.container():
        st.write("Recommendations")
        for i, art in enumerate(results, 1):
            st.write(f"{i}. {art['title']} (Similarity: {art['similarity']})")
            st.write(f"   Reference: {art['url']}")
            st.write()
        
        # Replace the button inside the results
        if st.button("Clear Results"):
            st.rerun()  # Force-refresh to reset

if __name__ == '__main__':
    placeholder = st.empty()
    
    # Initial screen (only shown if no results)
    with placeholder.container():
        st.markdown("# Aggrecrab ©")
        if st.button("RUN"):
            run()  # Generate results