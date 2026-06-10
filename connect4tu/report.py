import os
import sys
import requests

BASE_URL = "https://data.4tu.nl/v2"


def get_auth_headers():
    """Prepare Authorization header if TOKEN_4TU is set."""
    token = os.getenv("TOKEN_4TU")
    headers = {}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return headers


def fetch_articles(published_since, item_type=3, limit=100):
    """Fetch article records from the 4TU.ResearchData v2 API."""
    url = f"{BASE_URL}/articles"

    params = {
        "item_type": item_type,
        "limit": limit,
        "published_since": published_since,
    }

    headers = get_auth_headers()

    response = requests.get(
        url,
        params=params,
        headers=headers if headers else None,
        timeout=60,
    )
    response.raise_for_status()

    return response.json()


def fetch_article_details(uuid):
    """Fetch detailed metadata for one article/software/dataset record."""
    url = f"{BASE_URL}/articles/{uuid}"
    headers = get_auth_headers()

    response = requests.get(
        url,
        headers=headers if headers else None,
        timeout=60,
    )
    response.raise_for_status()

    return response.json()


def get_custom_field_value(custom_fields, field_name):
    """Return the value of a custom field by name."""
    for field in custom_fields:
        if field.get("name") == field_name:
            value = field.get("value", "")
            return value.strip() if isinstance(value, str) else value

    return ""


def has_non_empty_field(record, field_name):
    """Check whether a field exists and has a meaningful non-empty value."""
    value = record.get(field_name)

    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, list):
        return len(value) > 0

    if isinstance(value, dict):
        return len(value) > 0

    return True


def passes_required_field_filter(record, required_fields, mode="all"):
    """Check whether a record passes required field filters."""
    if not required_fields:
        return True

    checks = [has_non_empty_field(record, field) for field in required_fields]

    if mode == "any":
        return any(checks)

    return all(checks)


def is_archive_only_record(details):
    """Return True when all files are compressed archive files."""
    files = details.get("files", [])

    if not files:
        return False

    archive_extensions = (".zip", ".rar", ".tar.gz")

    return all(
        file_.get("mime_type", "").lower() == "application/zip"
        or file_.get("name", "").lower().endswith(archive_extensions)
        for file_ in files
    )


def generate_report(
    articles,
    item_type=3,
    required_fields=None,
    field_filter_mode="all",
    org_filter=None,
    format_filter=None,
):
    """Generate a Markdown report from fetched article records."""
    required_fields = required_fields or []

    item_type_label = "Software" if item_type == 9 else "Dataset"

    header_lines = []
    entry_lines = []
    included_count = 0

    for article in articles:
        uuid = article.get("uuid")
        title = article.get("title", "Untitled record")
        published = article.get("published_date", "unknown")

        try:
            details = fetch_article_details(uuid)

            if not passes_required_field_filter(
                details,
                required_fields=required_fields,
                mode=field_filter_mode,
            ):
                continue

            custom_fields = details.get("custom_fields", [])
            organization = get_custom_field_value(custom_fields, "Organizations")
            format_ = get_custom_field_value(custom_fields, "Format")

            if item_type == 3 and is_archive_only_record(details):
                continue

            if org_filter:
                if org_filter.lower() not in str(organization).lower():
                    continue

            if format_filter:
                format_list = [f.strip().lower() for f in str(format_).split(",")]
                if not any(format_filter.lower() in fmt for fmt in format_list):
                    continue

            description = details.get("description", "No description provided.")
            categories = details.get("categories", [])
            category_titles = [cat.get("title", "") for cat in categories]
            category_string = ", ".join(category_titles)

            resource_title = details.get("resource_title", "")
            resource_doi = details.get("resource_doi", "")

            included_count += 1

            entry_lines.append(f"## {included_count}. {title}\n")
            entry_lines.append(f"- UUID: `{uuid}`")
            entry_lines.append(f"- Published: {published}")
            entry_lines.append(f"- Item type: `{item_type}`")
            entry_lines.append(f"- DOI: {article.get('doi', 'N/A')}")
            entry_lines.append(f"- Resource title: {resource_title or 'N/A'}")
            entry_lines.append(f"- Resource DOI: {resource_doi or 'N/A'}")
            entry_lines.append(f"- Categories: {category_string or 'N/A'}")
            entry_lines.append(f"- Organizations: {organization or 'N/A'}")
            entry_lines.append(f"- Format: {format_ or 'N/A'}")

            entry_lines.append("\n### Description\n")
            entry_lines.append(f"{description or 'N/A'}\n")
            entry_lines.append("\n---\n")

        except Exception as error:
            entry_lines.append(f"## Error while processing: {title}\n")
            entry_lines.append(f"- UUID: `{uuid}`")
            entry_lines.append(f"- Error: Failed to fetch details: `{error}`")
            entry_lines.append("\n---\n")

    if included_count == 0:
        return "⚠️ No records matched the given filters.\n"

    header_lines.append(f"# 4TU.ResearchData {item_type_label} Report\n")
    header_lines.append(f"- Item type: `{item_type}`")
    header_lines.append(f"- Number of outputs in this report: `{included_count}`")
    header_lines.append(f"- Required fields: `{', '.join(required_fields) or 'None'}`")
    header_lines.append(f"- Field filter mode: `{field_filter_mode}`")
    header_lines.append("\n---\n")

    return "\n".join(header_lines + entry_lines)


def report_main(
    since,
    limit,
    output_path,
    item_type=3,
    required_fields=None,
    field_filter_mode="all",
    org_filter=None,
    format_filter=None,
):
    """Main entry point for the report CLI command."""
    try:
        articles = fetch_articles(
            published_since=since,
            item_type=item_type,
            limit=limit,
        )

        report = generate_report(
            articles=articles,
            item_type=item_type,
            required_fields=required_fields,
            field_filter_mode=field_filter_mode,
            org_filter=org_filter,
            format_filter=format_filter,
        )

        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(report)

        print(f"✅ Report saved to {output_path}")

    except Exception as error:
        print(f"❌ Error: {error}")
        sys.exit(1)