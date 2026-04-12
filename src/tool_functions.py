import requests
import pandas as pd


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
    return f"General information about {drug_name} is not yet available. Please ask a specific question such as its side effects, drug interactions, warnings, or pregnancy safety."