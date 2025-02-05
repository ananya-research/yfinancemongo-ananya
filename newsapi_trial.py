from newsapi.newsapi_client import NewsApiClient

#GIVES ERROR

# Init
newsapi = NewsApiClient(api_key='fe912f83727440c4b165db1f00c6a092')

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(
    q='bitcoin',
    category='business',
    language='en',
    country='us'
)



# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/top-headlines/sources
sources = newsapi.get_sources()