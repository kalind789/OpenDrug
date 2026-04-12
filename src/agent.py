from anthropic import Anthropic
from src.tool_functions import fda_api_call, check_cache
from src.utils import MVP_COLUMNS, SYSTEM_PROMPT
from src.tools_definition import tools
import os
from dotenv import load_dotenv
import streamlit as st


import os
import streamlit as st
from anthropic import Anthropic

# Works both locally and on Streamlit Cloud
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
except:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")

client = Anthropic(api_key=api_key)

def run_agent(user_query: str) -> str:
    """ Runs the agent with the given question and returns the response. """

    messages = [{"role": "user", "content": user_query}]

    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages
    )
    
    while response.stop_reason == "tool_use":
        tool_results = []

        for tool_call in response.content:
            if tool_call.type != "tool_use":
                continue

            if tool_call.name == "check_cache":
                tool_result = check_cache(
                    drug_name=tool_call.input["drug_name"]
                )

            elif tool_call.name == "fda_api_call":
                requested_fields = tool_call.input.get("fields", MVP_COLUMNS)
                fields = [f for f in requested_fields if f in MVP_COLUMNS]
                if not fields:
                    tool_result = "Sorry, that information is not yet available in this version of the app."
                else:
                    tool_result = fda_api_call(
                        drug_name=tool_call.input["drug_name"],
                        fields=fields
                    )

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": tool_result
            })

        # Claude response + all tool results to message history
        messages += [
            {"role": "assistant", "content": response.content},
            {"role": "user", "content": tool_results},
        ]

        # Claude reads the FDA data and writes final answer
        # This is with the new messages block from above
        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages
        )
    return response.content[0].text