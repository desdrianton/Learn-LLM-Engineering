import gradio as gr

def shout(text: str):
    print(f"Shout has been called with input {text}")
    return text.lower()

gr.Interface(fn=shout, inputs="textbox", outputs="textbox").launch()
