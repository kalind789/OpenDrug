import sqlite3
import requests
import pandas as pd
from src.utils import DB_PATH


CLINICAL_FIELDS = [
    'boxed_warning',
    'indications_and_usage',
    'contraindications',
    'warnings_and_cautions',
    'warnings',
    'adverse_reactions',
    'drug_interactions',
    'pregnancy',
    'pregnancy_or_breast_feeding',
    'use_in_specific_populations',
    'ask_doctor',
    'ask_doctor_or_pharmacist',
]

def fda_api_call(drug_name):
    """ Calls the FDA API to get clinical label information for the drug. """
    response = requests.get(f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:\"{drug_name}\"&limit=1")

    if response.status_code == 404:
        return "Drug not found in FDA database. Please check the spelling or try the generic name."

    data = pd.DataFrame(response.json()['results'])
    target_fields = CLINICAL_FIELDS
    available_fields = [f for f in target_fields if f in data.columns]
    if not available_fields:
        return "No clinical information is available for this drug in the FDA database."

    needed_data = data[available_fields]
    rows = needed_data.to_dict(orient='records')
    drug_string = "\n\n".join(
        f"{k.replace('_', ' ').upper()}:\n{v[0] if isinstance(v, list) else v}"
        for row in rows for k, v in row.items()
    )
    return drug_string

def check_cache(drug_name):
    try:
        conn = sqlite3.connect(DB_PATH)
        row = conn.execute(
            "SELECT summary FROM drug_summaries WHERE drug_name = ?",
            (drug_name.lower(),)
        ).fetchone()
        conn.close()
        if row:
            return row[0]
    except Exception:
        pass
    return (
        f"General information about {drug_name} is not available in our database. "
        "Please ask a specific question such as its side effects, drug interactions, "
        "warnings, or pregnancy safety."
    )