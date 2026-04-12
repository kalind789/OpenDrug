import requests
import pandas as pd


def fda_api_call(drug_name, fields):
    """ Calls the FDA API to get the relevant fields for the drug. """
    response = requests.get(f"https://api.fda.gov/drug/label.json?search=openfda.generic_name:\"{drug_name}\"&limit=1")

    # If the drug is not found, return a message indicating that
    if response.status_code == 404:
        return "Drug not found in FDA database. Please check the spelling or try the generic name."
    
    # Else, process the response and return the relevant fields
    data = pd.DataFrame(response.json()['results'])
    needed_data = data[fields]
    needed_list = needed_data.values.tolist()
    drug_string = "\n".join([str(item) for item in needed_list])

    return drug_string

def check_cache(drug_name):
    return f"General information about {drug_name} is not yet available. Please ask a specific question such as its side effects, drug interactions, warnings, or pregnancy safety."