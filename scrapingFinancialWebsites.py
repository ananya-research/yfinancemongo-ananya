# import requests
# from bs4 import BeautifulSoup
# import json
# import boto3

# # --- Helper Function to Fetch Article Content ---
# def fetch_article_content(link):
#     headers = {
#         "User-Agent": (
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#             "AppleWebKit/537.36 (KHTML, like Gecko) "
#             "Chrome/115.0.0.0 Safari/537.36"
#         )
#     }
#     try:
#         response = requests.get(link, headers=headers)
#         if response.status_code != 200:
#             print("Error fetching article content:", response.status_code)
#             return ""
#         soup = BeautifulSoup(response.text, 'html.parser')
#         # Attempt to extract the main content using a common Yahoo Finance container.
#         content_div = soup.find('div', class_='caas-body')
#         if content_div:
#             content = content_div.get_text(separator="\n", strip=True)
#         else:
#             # Fallback: extract all paragraphs from the page.
#             paragraphs = soup.find_all('p')
#             content = "\n".join(p.get_text(strip=True) for p in paragraphs)
#         return 
#     except Exception as e:
#         print("Exception while fetching article content:", e)
#         return ""

# # --- Function to Scrape Yahoo Finance News ---
# def scrape_yahoo_finance_news():
#     url = "https://finance.yahoo.com/stock-market-news"
#     headers = {
#         "User-Agent": (
#             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
#             "AppleWebKit/537.36 (KHTML, like Gecko) "
#             "Chrome/115.0.0.0 Safari/537.36"
#         )
#     }
#     response = requests.get(url, headers=headers)
#     if response.status_code != 200:
#         print("Error fetching Yahoo Finance news:", response.status_code)
#         return []
    
#     soup = BeautifulSoup(response.text, 'html.parser')
#     articles = []
    
#     # Look for headlines within <h3> tags; then grab the link and fetch the article content.
#     for h3 in soup.find_all('h3'):
#         headline = h3.get_text(strip=True)
#         parent_a = h3.find_parent('a')
#         link = None
#         if parent_a and parent_a.has_attr('href'):
#             link = parent_a['href']
#             if link.startswith('/'):
#                 link = "https://finance.yahoo.com" + link
#         if headline and link:
#             content = fetch_article_content(link)
#             if content:
#                 articles.append({
#                     "headline": headline,
#                     "link": link,
#                     "content": content
#                 })
#     return articles

# # --- Function to Upload Data to S3 ---
# def upload_to_s3(data, bucket_name, object_name):
#     s3_client = boto3.client('s3')
#     try:
#         s3_client.put_object(
#             Body=json.dumps(data, indent=2),
#             Bucket=bucket_name,
#             Key=object_name,
#             ContentType='application/json'
#         )
#         print(f"Successfully uploaded data to s3://{bucket_name}/{object_name}")
#     except Exception as e:
#         print("Error uploading to S3:", e)

# if __name__ == "__main__":
#     # Scrape the news articles.
#     news_articles = scrape_yahoo_finance_news()
    
#     # Option 1: Save locally.
#     with open("yahoo_finance_articles.json", "w", encoding="utf-8") as f:
#         json.dump(news_articles, f, ensure_ascii=False, indent=2)
#     print(f"Saved {len(news_articles)} articles locally to yahoo_finance_articles.json")
    
#     # Option 2: Upload directly to an S3 bucket.
#     # Replace 'your-bucket-name' with the name of your S3 bucket.
#     BUCKET_NAME = 'yfinance-news-trial'
#     OBJECT_NAME = 'yahoo_finance_articles.json'
#     upload_to_s3(news_articles, BUCKET_NAME, OBJECT_NAME)


import requests
from bs4 import BeautifulSoup
import json

def fetch_article_content(link):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(link, headers=headers)
        if response.status_code != 200:
            print(f"Error fetching article content from {link}: {response.status_code}")
            return ""
        soup = BeautifulSoup(response.text, "html.parser")
        # Try to extract the main content container; Yahoo Finance often uses 'caas-body'
        content_div = soup.find("div", class_="caas-body")
        if content_div:
            content = content_div.get_text(separator="\n", strip=True)
        else:
            # Fallback: get text from all <p> tags
            paragraphs = soup.find_all("p")
            content = "\n".join(p.get_text(strip=True) for p in paragraphs)
        return content
    except Exception as e:
        print(f"Exception while fetching article content from {link}: {e}")
        return ""

def scrape_yahoo_finance_stock_market_news():
    url = "https://finance.yahoo.com/topic/stock-market-news/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Error fetching Yahoo Finance Stock Market News page:", response.status_code)
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    
    # Locate article headlines; Yahoo Finance typically wraps headlines in <h3> tags
    for h3 in soup.find_all("h3"):
        headline = h3.get_text(strip=True)
        parent_a = h3.find_parent("a")
        link = None
        if parent_a and parent_a.has_attr("href"):
            link = parent_a["href"]
            # If the link is relative, prepend the base URL.
            if link.startswith("/"):
                link = "https://finance.yahoo.com" + link
        if headline and link:
            print(f"Processing article: {headline}")
            content = fetch_article_content(link)
            if content:
                articles.append({
                    "headline": headline,
                    "link": link,
                    "content": content
                })
    return articles

if __name__ == "__main__":
    news_articles = scrape_yahoo_finance_stock_market_news()
    # Save the scraped articles to a local JSON file.
    with open("yahoo_finance_stock_market_articles.json", "w", encoding="utf-8") as f:
        json.dump(news_articles, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(news_articles)} articles to yahoo_finance_stock_market_articles.json")
