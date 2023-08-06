if __name__ == "__main__":
    from requests import session as S

def search(url: str, keyword: str):
    ret = S().get(url= url, params= {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": keyword
    }).json()

    pages = ret['query']['search']
    search_result = [ {'title': page['title'], 'summary': page['snippet']} for page in pages ]

    return search_result
