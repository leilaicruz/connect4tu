
import requests
import pandas as pd
import os

def fetch_articles(api_token, base_url="https://data.4tu.nl", endpoint="/v2/articles"):
    url = base_url + endpoint
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    params = {"published_since": 20250101, "limit": 10, "item_type": 9}
    response = requests.get(url, headers=headers, params=params)
    
    if response.ok:
        articles_json = response.json()
        desired_columns = [
            "title", "doi", "url", "published_date", "defined_type", 
            "defined_type_name", "url_private_api", "url_public_api", 
            "url_private_html", "url_public_html"
        ]
        filtered_articles = [
            {col: article.get(col, None) for col in desired_columns}
            for article in articles_json
        ]
        df = pd.DataFrame(filtered_articles)
        print(df)
        return df
    else:
        print("Error:", response.status_code, response.text)
        return None

def fetch_main():
    token = os.getenv("DJEHUTY_API_TOKEN")
    if not token:
        raise ValueError("DJEHUTY_API_TOKEN not found in environment variables.")
    fetch_articles(token)
