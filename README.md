
# connect4tu

`connect4tu` is a Python package that provides a command-line interface (CLI) to interact with the [4TU.ResearchData API](https://djehuty.4tu.nl/#x1-600005). It supports uploading datasets, fetching recent articles, and generating Markdown reports.

---

## 📦 Installation

First, clone or download this package, unzip it, and navigate to the folder.

We recommend using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

This installs the `connect4tu` CLI in editable mode.

---

## 🔐 Setting Up Your Token

Only the **upload** command requires authentication. You need to set the `API_TOKEN` via a shell script:

1. Create a file called `set_env.sh`:

```bash
echo 'export API_TOKEN="your_actual_token_here"' > set_env.sh
chmod +x set_env.sh
```

2. Add it to your `.gitignore` to keep it private.

---

## 🚀 Usage

### Upload a Dataset

```bash
connect4tu upload example_metadata.yaml --env_script set_env.sh
```

Optional arguments:
- `--base_url`: Custom API URL (default: `https://next.data.4tu.nl`)
- `--endpoint`: Upload endpoint (default: `/v2/account/articles`)

---

### Fetch Recent Datasets (No Token Needed)

```bash
connect4tu fetch
```

This prints a quick table of recent articles published on 4TU.ResearchData.

---

### Generate a Markdown Report

```bash
connect4tu report --since 2025-03-01 --limit 20 --organization-filter "Delft" --format-filter "NetCDF" --output tud_netcdf_report.md
```

Options:
- `--since`: Date in `YYYY-MM-DD` format
- `--limit`: Max number of records to fetch
- `--organization-filter`: Filter by organization name (from metadata)
- `--format-filter`: Filter by dataset format (from metadata)
- `--output`: Output path for the report

---

## 🧠 Project Structure

```
connect4tu/
├── connect4tu/
│   ├── cli.py
│   ├── upload.py
│   ├── fetch.py
│   ├── report.py
│   └── env_utils.py
├──────secrets/
        ├── set_env.sh (user-defined, not included)
├── pyproject.toml
├── README.md
├── .gitignore
├── example_metadata.yaml

```

---

## 🧪 Testing Your Installation

```bash
connect4tu fetch
connect4tu report --output test.md
```




