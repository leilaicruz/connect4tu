
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

To setup your api private token as environmental variables

- Create a `.env` file at the root of your project
- Write in the following format your private token(s) 
`TOKEN_xx=BLABLABLABLABLBALBA`
- Type in the terminal `source .env`
- Then anywhere you use the token as part of your API call , use `${TOKEN_xx}` to invoke it. 


- Add it to your `.gitignore` to keep it private.

---

## 🚀 Usage

> **Important:**  
> Before using the CLI, create a `.env` file at the root of your project with your API tokens:
> ```bash
> # Example .env file
> NEXT_API_TOKEN=your_token_for_next_data_4tu
> TOKEN_4TU=your_token_for_data_4tu
> ```

---

### Upload a Dataset (Requires Token)

```bash

connect4tu upload metadata_upload_dataset.yaml

```

Optional arguments:
- `--base_url`: Custom API URL (default: `https://next.data.4tu.nl`)
- `--endpoint`: Upload endpoint (default: `/v2/account/articles`)

The token (`NEXT_API_TOKEN`) will be automatically read from the `.env` file.

---

### Fetch Recent Datasets (Public or Private)

```bash
connect4tu fetch
```

- If `TOKEN_4TU` is available in `.env`, private datasets will also be accessible.
- If no token is set, only public datasets will be listed.

---

### Generate a Markdown Report

```bash
connect4tu report --since 2025-03-01 --limit 20 --organization-filter "Delft" --format-filter "NetCDF" --output connect4tu/outputs/tud_netcdf_report.md
```

Options:
- `--since`: Date in `YYYY-MM-DD` format
- `--limit`: Maximum number of records to fetch
- `--organization-filter`: Filter by organization name (from dataset metadata)
- `--format-filter`: Filter by dataset format (from dataset metadata)
- `--output`: Output path for the generated Markdown report

The report tool will also use the `TOKEN_4TU` if available, to fetch private or unpublished datasets.

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




