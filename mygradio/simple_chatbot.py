import gradio as gr

from core.llm_connector import ChatGPTConnector

llm_connector = ChatGPTConnector()

def chat(message, history):
    system_prompt = ""

    return llm_connector.ask(system_prompt=system_prompt, user_prompt=message)

gr.ChatInterface(fn=chat, type="messages").launch()
