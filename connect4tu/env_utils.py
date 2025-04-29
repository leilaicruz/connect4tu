import os

def load_env_from_script(env_path=".env"):
    """
    Loads environment variables from a .env file into the current Python process.
    Expected format: KEY=VALUE, one per line.
    """
    if not os.path.exists(env_path):
        raise FileNotFoundError(f".env file not found at {env_path}")

    with open(env_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip comments and blank lines
            if "=" not in line:
                continue  # Skip malformed lines

            key, value = line.split("=", 1)
            os.environ[key.strip()] = value.strip()

