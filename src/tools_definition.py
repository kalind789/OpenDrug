tools = [
    {
        "name": "fda_api_call",
        "description": "Get FDA drug information given the drug name and fields",
        "input_schema": {
            "type": "object",
            "properties": {
                "drug_name": {
                    "type": "string",
                    "description": "The name of the drug to look up.",
                },
                "fields": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "The fields to retrieve from the FDA API."
                }
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