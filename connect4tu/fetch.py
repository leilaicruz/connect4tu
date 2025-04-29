import requests
import pandas as pd
import os

def fetch_articles(base_url="https://data.4tu.nl", endpoint="/v2/articles"):
    url = base_url + endpoint

    # Prepare parameters
    params = {
        "published_since": 20250101,
        "limit": 10,
        "item_type": 9
    }

    # Check for optional token
    token = os.getenv("TOKEN_4TU")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = requests.get(url, params=params, headers=headers if headers else None, timeout=60)

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
    fetch_articles()
