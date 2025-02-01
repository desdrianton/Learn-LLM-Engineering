import gradio as gr
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from agent.brochure_maker_agent import BrochureMakerAgent
from core.llm_connector import ChatGPTConnector

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4o-mini"
openai = OpenAI()
llm_connector = ChatGPTConnector()
brochure_maker_agent = BrochureMakerAgent(llm_connector)

def create_brochure(url: str) -> str:
    return brochure_maker_agent.with_params({"url": url}).act()

create_brochure_function_desc = {
    "name": "create_brochure",
    "description": "Create a company brochure from url",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "The url that user want to make the brochure",
            },
        },
        "required": ["url"],
        "additionalProperties": False
    }
}


def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    url = arguments.get('url')
    brochure = create_brochure(url)
    response = {
        "role": "tool",
        "content": json.dumps({"url": url,"brochure": brochure}),
        "tool_call_id": tool_call.id
    }
    return response, brochure


def chat(message, history):
    system_prompt = ""
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

    tools = [{"type": "function", "function": create_brochure_function_desc}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response, brochure = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)

    return response.choices[0].message.content


gr.ChatInterface(fn=chat, type="messages").launch()
