import argparse
from .upload import upload_main
from .fetch import fetch_main
from .report import report_main
from .env_utils import load_env_from_script

def main():
    # Load environment variables from .env at startup
    load_env_from_script()

    parser = argparse.ArgumentParser(prog="connect4tu", description="CLI for 4TU.ResearchData API")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Upload subcommand
    upload_parser = subparsers.add_parser("upload", help="Upload a dataset")
    upload_parser.add_argument("yaml_file", help="Path to the metadata YAML file")
    upload_parser.add_argument("--base_url", type=str, default="https://next.data.4tu.nl")
    upload_parser.add_argument("--endpoint", type=str, default="/v2/account/articles")

    # Fetch subcommand
    fetch_parser = subparsers.add_parser("fetch", help="Quick fetch and list recent articles")

    # Report subcommand
    report_parser = subparsers.add_parser("report", help="Generate a filtered Markdown report of datasets")
    report_parser.add_argument("--since", type=str, default="2025-03-01", help="Start date in YYYY-MM-DD format")
    report_parser.add_argument("--limit", type=int, default=10, help="Number of datasets to fetch")
    report_parser.add_argument("--output", type=str, default="dataset_report.md", help="Output file for Markdown report")
    report_parser.add_argument("--organization-filter", type=str, help="Filter datasets by organization name")
    report_parser.add_argument("--format-filter", type=str, help="Filter datasets by file format")
    report_parser.add_argument("--item-type",type=int,default=3,help="4TU item type to fetch: 3 for datasets, 9 for software")

    report_parser.add_argument(
        "--require-field",
        action="append",
        default=[],
        help=(
            "Only include records where this field is present and non-empty. "
            "Can be used multiple times, e.g. --require-field resource_title "
            "--require-field resource_doi"
        )
    )

    report_parser.add_argument(
        "--field-filter-mode",
        choices=["all", "any"],
        default="all",
        help=(
            "How to combine multiple --require-field filters. "
            "'all' requires all fields; 'any' requires at least one."
        )
    )

    args = parser.parse_args()

    if args.command == "upload":
        upload_main(args.yaml_file, args.base_url, args.endpoint,api_token=None)
    elif args.command == "fetch":
        fetch_main()
    elif args.command == "report":
        report_main(
        since=args.since,
        limit=args.limit,
        output_path=args.output,
        item_type=args.item_type,
        required_fields=args.require_field,
        field_filter_mode=args.field_filter_mode,
        org_filter=args.organization_filter,
        format_filter=args.format_filter,
    )

if __name__ == "__main__":
    main()
