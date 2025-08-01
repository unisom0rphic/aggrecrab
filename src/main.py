import streamlit as st

import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("main.log")]
)
logger = logging.getLogger(__name__)

from articleRecommender import ArticleRecommender, RSSFetchError

class RecommendationError(Exception):
    pass

def run(request: str):
    """Run recommendations and manage UI state"""
    recommender = ArticleRecommender(request)
    logger.info("Started recommendation search")
    with st.spinner("Finding good articles..."):
        try:
            results = recommender.run()
        except RSSFetchError as e:
            logger.error("Recommendation search failed: %s", str(e), exc_info=True)
            raise RecommendationError(f"Recommendation search failed: {str(e)}") from e
    
    with placeholder.container():
        logger.info("Succesfully found recommendations")
        st.write("Recommendations")
        for i, art in enumerate(results, 1):
            st.write(f"{i}. {art['title']} (Similarity: {art['similarity']})")
            st.write(f"   Reference: {art['url']}")
            st.write()
        
        # FIXME: rendering issues
        # Doesn't reload the page, instead merges both pages (main and results) for a brief moment
        # Could be a streamlit issue, haven't found a good way to prevent this yet
        if st.button("Clear Results"):
            logger.info("User reloags the page")
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
