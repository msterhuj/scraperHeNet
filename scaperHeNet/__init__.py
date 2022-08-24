from pathlib import Path

# init all data directories for scraping and parsing

dir_type = [
    "data/html",
    "data/json",
]

dir_data = [
    "report_world",
    "asn",
]

for dt in dir_type:
    for dd in dir_data:
        Path(f"{dt}/{dd}").mkdir(parents=True, exist_ok=True)
