from articleRecommender import ArticleRecommender

if __name__ == "__main__":
    # Пример config.yaml:
    # sources:
    #   - "https://example1.com/rss"
    #   - "https://example2.com/rss"
    # anchor_text: "технологии искусственный интеллект python"
    # top_n: 10
    
    recommender = ArticleRecommender("config.yaml")
    results = recommender.run()
    
    print("Топ рекомендаций:")
    for i, art in enumerate(results, 1):
        print(f"{i}. {art['title']} (Сходство: {art['similarity']})")
        print(f"   Ссылка: {art['url']}")
        print()