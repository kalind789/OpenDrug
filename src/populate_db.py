"""
Populates the SQLite drug cache with summaries of the top 15 most prescribed
drugs in the USA. Fetches raw data from the FDA API and uses Claude to generate
plain-English summaries based solely on that data.

Run from the project root:
    python -m src.populate_db
"""

import sqlite3
import os
from datetime import datetime
from anthropic import Anthropic
from dotenv import load_dotenv
from src.tool_functions import fda_api_call
from src.utils import DB_PATH, TOP_DRUGS

load_dotenv()

SUMMARY_SYSTEM_PROMPT = """You are a medical information summarizer.
Your ONLY job is to write a plain-English summary of a drug based strictly on
the FDA label text provided to you. You must not add, infer, or fill in any
information that is not explicitly present in the text. If a section is missing
from the FDA text, omit it entirely from your summary — do not guess.

Structure your summary using only these sections, and only include a section if
the information appears in the provided text:
- What it is used for
- Key warnings
- Common side effects
- Drug interactions
- Pregnancy and special populations
"""


def setup_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drug_summaries (
            drug_name   TEXT PRIMARY KEY,
            summary     TEXT NOT NULL,
            raw_fda_data TEXT NOT NULL,
            fetched_at  TEXT NOT NULL
        )
    """)
    conn.commit()


def summarize_with_claude(client, drug_name, raw_fda_data):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=SUMMARY_SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": (
                f"Here is the FDA label data for {drug_name}:\n\n"
                f"{raw_fda_data}\n\n"
                "Summarize this drug using only the text above."
            )
        }]
    )
    return response.content[0].text


def populate():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set.")

    client = Anthropic(api_key=api_key)
    conn = sqlite3.connect(DB_PATH)
    setup_db(conn)

    for drug in TOP_DRUGS:
        print(f"Processing {drug}...")
        raw_data = fda_api_call(drug)

        if "not found" in raw_data.lower() or "no clinical information" in raw_data.lower():
            print(f"  Skipping {drug}: FDA data unavailable.")
            continue

        summary = summarize_with_claude(client, drug, raw_data)

        conn.execute(
            """
            INSERT OR REPLACE INTO drug_summaries (drug_name, summary, raw_fda_data, fetched_at)
            VALUES (?, ?, ?, ?)
            """,
            (drug.lower(), summary, raw_data, datetime.utcnow().isoformat())
        )
        conn.commit()
        print(f"  Stored: {drug}")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    populate()
