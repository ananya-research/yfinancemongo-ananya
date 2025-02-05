import json
import spacy
from transformers import pipeline

def load_articles(filename):
    """
    Load articles from a JSON file.
    The file should contain a list of articles, each with keys such as "headline", "link", and "content".
    """
    with open(filename, "r", encoding="utf-8") as f:
        articles = json.load(f)
    return articles

def process_article(article, nlp, sentiment_pipeline, summarizer):
    """
    Process a single article by:
    - Extracting named entities using spaCy.
    - Analyzing sentiment using a Hugging Face sentiment pipeline.
    - Summarizing the article (if long enough) using a summarization pipeline.
    
    Returns a dictionary with the original headline and link, plus the NLP results.
    """
    content = article.get("content", "")
    
    # Perform Named Entity Recognition (NER) with spaCy
    doc = nlp(content)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Perform Sentiment Analysis (we use only the first 512 characters for performance)
    sentiment_result = sentiment_pipeline(content[:512])
    sentiment = sentiment_result[0]  # e.g., {"label": "POSITIVE", "score": 0.98}
    
    # Summarization: only if content has more than 100 words
    words = content.split()
    if len(words) > 100:
        # Summarization models can have input length restrictions so we use the full text or a truncated version
        summary_result = summarizer(content, max_length=130, min_length=30, do_sample=False)
        summary = summary_result[0]["summary_text"]
    else:
        summary = content
    
    return {
        "headline": article.get("headline"),
        "link": article.get("link"),
        "entities": entities,
        "sentiment": sentiment,
        "summary": summary
    }

def main():
    # Change the filename if needed – this is where your scraped data is stored.
    input_filename = "yahoo_finance_stock_market_articles.json"
    output_filename = "news_nlp_results.json"
    
    print(f"Loading articles from {input_filename}...")
    articles = load_articles(input_filename)
    print(f"Loaded {len(articles)} articles.")
    
    # Initialize NLP pipelines
    print("Initializing NLP models...")
    nlp = spacy.load("en_core_web_sm")
    sentiment_pipeline_model = pipeline("sentiment-analysis")
    summarizer_model = pipeline("summarization")
    
    # Process each article
    print("Processing articles...")
    processed_articles = []
    for article in articles:
        processed = process_article(article, nlp, sentiment_pipeline_model, summarizer_model)
        processed_articles.append(processed)
    
    # Save the results to a new JSON file
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(processed_articles, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {len(processed_articles)} articles and saved NLP results to {output_filename}.")

if __name__ == "__main__":
    main()
