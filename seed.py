import json
from database import add_entry, get_all_entries

def seed():
    if get_all_entries():
        print("Already seeded")
        return

    with open("data.json", "r", encoding="utf-8") as f:
        entries = json.load(f)

    for entry in entries:
        add_entry(entry["title"], entry["body"], entry["isoTime"], entry["lat"], entry["lon"])

    print(f"Added {len(entries)} entries")

if __name__ == "__main__":
    seed()
