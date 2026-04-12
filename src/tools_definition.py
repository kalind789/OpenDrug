tools = [
    {
        "name": "fda_api_call",
        "description": "Get clinical FDA label information for a drug, including warnings, side effects, drug interactions, pregnancy safety, and indications.",
        "input_schema": {
            "type": "object",
            "properties": {
                "drug_name": {
                    "type": "string",
                    "description": "The generic name of the drug to look up.",
                },
            },
            "required": ["drug_name"],
        },
    },
    {
        "name": "check_cache",
        "description": "Get information for a general question about a drug",
        "input_schema": {
            "type": "object",
            "properties": {
                "drug_name": {
                    "type": "string",
                    "description": "The name of the drug to look up in the cache.",
                }
            },
            "required": ["drug_name"],
        },
    },
]