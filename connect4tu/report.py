import requests
from datetime import datetime
import os
import sys

BASE_URL = "https://data.4tu.nl/v2"

def get_auth_headers():
    """Prepare Authorization header if TOKEN_4TU is set."""
    token = os.getenv("TOKEN_4TU")
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def fetch_recent_datasets(published_since, item_type=3, limit=100):
    url = f"{BASE_URL}/articles"
    params = {
        "item_type": item_type,
        "limit": limit,
        "published_since": published_since
    }
    headers = get_auth_headers()
    response = requests.get(url, params=params, headers=headers if headers else None, timeout=60)
    response.raise_for_status()
    return response.json()

def fetch_dataset_details(uuid):
    url = f"{BASE_URL}/articles/{uuid}"
    headers = get_auth_headers()
    response = requests.get(url, headers=headers if headers else None, timeout=60)
    response.raise_for_status()
    return response.json()

def get_custom_field_value(custom_fields, field_name):
    for field in custom_fields:
        if field.get("name") == field_name:
            return field.get("value", "").strip()
    return ""

def generate_report(datasets, org_filter=None, format_filter=None):
    report_lines = []
    included_count = 0
    for dataset in datasets:
        uuid = dataset.get("uuid")
        title = dataset.get("title")
        published = dataset.get("published_date", "unknown")
        try:
            details = fetch_dataset_details(uuid)
            description = details.get("description", "No description provided.")
            categories = details.get("categories", [])
            category_titles = [cat.get("title", "") for cat in categories]
            category_string = ", ".join(category_titles)
            custom_fields = details.get("custom_fields", [])
            organization = get_custom_field_value(custom_fields, "Organizations")
            format_ = get_custom_field_value(custom_fields, "Format")

            # Skip datasets that only contain ZIP files
            files = details.get("files", [])
            if files:
                only_zip_files = all(
                    f.get("mime_type", "").lower() == "application/zip" or
                    f.get("name", "").lower().endswith(".zip") or 
                    f.get("name", "").lower().endswith(".rar") or 
                    f.get("name", "").lower().endswith(".tar.gz")
                    for f in files
                )
                if only_zip_files:
                    continue  # Skip this dataset

            if org_filter and format_filter:
                org_condition = org_filter.lower() in organization.lower()
                format_list = [f.strip().lower() for f in format_.split(",")]
                format_condition = any(format_filter.lower() in fmt for fmt in format_list)

                if not (org_condition and format_condition):
                    continue
            elif org_filter:
                if org_filter.lower() not in organization.lower():
                    continue
            elif format_filter:
                format_list = [f.strip().lower() for f in format_.split(",")]
                if not any(format_filter.lower() in fmt for fmt in format_list):
                    continue



            included_count += 1

        except Exception as e:
            description = "Failed to fetch details."
            category_string = "N/A"
            organization = "N/A"
            format_ = "N/A"

        report_lines.append(f"## {title}\n")
        report_lines.append(f"- UUID: `{uuid}`")
        report_lines.append(f"- Published: {published}")
        report_lines.append(f"- Description: {description}")
        report_lines.append(f"- Categories: {category_string}")
        report_lines.append(f"- Organizations: {organization}")
        report_lines.append(f"- Format: {format_}")
        report_lines.append(f"- DOI: [Link]({dataset.get('doi')})")
        report_lines.append("\n---\n")

    if included_count == 0:
        return "⚠️ No datasets matched the given filters.\n"

    return "\n".join(report_lines)

def report_main(since, limit, output_path, org_filter=None, format_filter=None):
    try:
        datasets = fetch_recent_datasets(since, limit=limit)
        report = generate_report(datasets, org_filter=org_filter, format_filter=format_filter)
        # Ensure parent directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w") as f:
            f.write(report)

        
        print(f"✅ Report saved to {output_path}")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
