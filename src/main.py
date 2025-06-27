from articleRecommender import ArticleRecommender

if __name__ == "__main__":
    # Example config.yaml:
    # sources:
    #   - "https://example1.com/rss"
    #   - "https://example2.com/rss"
    # anchor_text: "technology artificial intelligence python"
    # top_n: 10
    
    recommender = ArticleRecommender("config.yaml")
    results = recommender.run()
    
    print("Recommendations")
    for i, art in enumerate(results, 1):
        print(f"{i}. {art['title']} (Similarity: {art['similarity']})")
        print(f"   Reference: {art['url']}")
        print()