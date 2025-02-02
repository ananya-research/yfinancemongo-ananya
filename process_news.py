import json
import spacy
from transformers import pipeline

# Load the pre-trained spaCy model for NER
nlp = spacy.load("en_core_web_sm")

# Initialize Hugging Face pipelines for sentiment analysis and summarization
sentiment_pipeline = pipeline("sentiment-analysis")
summarization_pipeline = pipeline("summarization")

def process_article(article):
    content = article.get("content", "")
    
    # Named Entity Recognition (NER) using spaCy
    doc = nlp(content)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Sentiment Analysis (process the first 512 characters to avoid input length issues)
    sentiment = sentiment_pipeline(content[:512])
    
    # Summarization: use the summarizer only if the content is long enough (e.g., over 100 words)
    words = content.split()
    if len(words) > 100:
        # Hugging Face summarization models may require shorter input, so you might need to truncate or chunk text
        summary_result = summarization_pipeline(content, max_length=130, min_length=30, do_sample=False)
        summary = summary_result[0]["summary_text"]
    else:
        summary = content

    # Return the processed article data as a new dictionary
    processed = {
        "headline": article.get("headline"),
        "link": article.get("link"),
        "content": content,
        "entities": entities,
        "sentiment": sentiment,
        "summary": summary
    }
    return processed

def main():
    # Load the scraped articles from the local JSON file
    with open("yahoo_finance_articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    
    processed_articles = [process_article(article) for article in articles]
    
    # Save the processed data into a new JSON file
    with open("processed_yahoo_finance_articles.json", "w", encoding="utf-8") as f:
        json.dump(processed_articles, f, ensure_ascii=False, indent=2)
    
    print(f"Processed {len(processed_articles)} articles and saved to processed_yahoo_finance_articles.json")

if __name__ == "__main__":
    main()
