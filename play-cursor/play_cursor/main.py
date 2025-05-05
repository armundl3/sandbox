from fastapi import FastAPI
import gradio as gr

app = FastAPI(title="Play Cursor API")

def greet(name):
    return f"Hello {name}!"

# Create Gradio interface
demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="Enter your name"),
    outputs=gr.Textbox(label="Greeting"),
    title="Hello World App",
    description="Enter your name and get a greeting!"
)

# Mount Gradio app to FastAPI
app = gr.mount_gradio_app(app, demo, path="/")