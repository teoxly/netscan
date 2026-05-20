import json
import csv
from pathlib import Path


def save_json(data, filename: str):
    Path(filename).write_text(json.dumps(data, indent=2), encoding="utf-8")


def save_csv(open_ports, filename: str):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["port", "service", "banner"])
        for p in open_ports:
            writer.writerow([p["port"], p["service"], p["banner"] or ""])