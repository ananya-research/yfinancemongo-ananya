import time
import schedule
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

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
        content_div = soup.find("div", class_="caas-body")
        if content_div:
            content = content_div.get_text(separator="\n", strip=True)
        else:
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
    
    for h3 in soup.find_all("h3"):
        headline = h3.get_text(strip=True)
        parent_a = h3.find_parent("a")
        link = None
        if parent_a and parent_a.has_attr("href"):
            link = parent_a["href"]
            if link.startswith("/"):
                link = "https://finance.yahoo.com" + link
        if headline and link:
            content = fetch_article_content(link)
            if content:
                articles.append({
                    "headline": headline,
                    "link": link,
                    "content": content,
                    "timestamp": datetime.utcnow().isoformat()
                })
    return articles

def job():
    articles = scrape_yahoo_finance_stock_market_news()
    if articles:
        # Save the latest batch to a JSON file, appending a timestamp in the filename.
        filename = f"yahoo_finance_articles_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(articles)} articles to {filename}")
    else:
        print("No new articles found.")

# Schedule the job to run every minute
schedule.every(1).minutes.do(job)

if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
