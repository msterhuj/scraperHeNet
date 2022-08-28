from pathlib import Path

# init all data directories for scraping and parsing

data_dir = [
    "data/html/report_world",
    "data/html/asn",
    "data/html/range",
    "data/json",
]

for dd in data_dir:
    Path(f"{dd}").mkdir(parents=True, exist_ok=True)
