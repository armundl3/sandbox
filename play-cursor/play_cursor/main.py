import os
import logging
from fastapi import FastAPI
import gradio as gr
import requests
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "mistral")

logger.info(f"Starting Play Cursor API with Ollama model: {OLLAMA_MODEL}")

app = FastAPI(title="Play Cursor API")

def get_ollama_response(prompt):
    logger.info(f"Sending prompt to Ollama: {prompt}")
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt
            }
        )
        if response.status_code == 200:
            result = ""
            for chunk in response.iter_lines():
                if chunk:
                    try:
                        import json
                        data = json.loads(chunk)
                        result += data.get("response", "")
                    except Exception as e:
                        logger.warning(f"Failed to parse Ollama response chunk: {e}")
                        continue
            logger.info("Received response from Ollama.")
            return result
        else:
            logger.error(f"Ollama returned status code {response.status_code}: {response.text}")
            return "(Could not get a response from Ollama)"
    except Exception as e:
        logger.error(f"Error communicating with Ollama: {e}")
        return "(Could not get a response from Ollama)"

def greet_haiku_fact(name, topic):
    greeting = f"Hello {name}!"
    haiku = ""
    fact = ""
    if topic:
        haiku_prompt = (
            f"Give me a random fact about {topic} in the form of a haiku. "
            "Respond with only the haiku, no explanation."
        )
        fact_prompt = (
            f"Give me a random made up but completey believble fact about {topic}. Respond with only the made up fact, no explanation. Make it believable."
        )
        haiku = get_ollama_response(haiku_prompt)
        fact = get_ollama_response(fact_prompt)
    else:
        logger.debug("No topic provided by user.")
    return greeting, haiku, fact

# Gradio interface
theme = gr.themes.Default().set(
    button_primary_background_fill="#808000",
    button_primary_background_fill_hover="#6b6b00",  # slightly darker on hover
    button_primary_text_color="white"
)
with gr.Blocks(theme=theme) as demo:
    gr.Markdown(f"# Hello World + Haiku Facts Generator with Ollama + {OLLAMA_MODEL}")
    name = gr.Textbox(label="Enter your name")
    topic = gr.Textbox(label="Enter a topic to get a random fact")
    submit_btn = gr.Button("Submit")
    greeting_out = gr.Textbox(label="Greeting")
    with gr.Row():
        haiku_out = gr.Textbox(label="Snack Facts (Haiku)")
        fact_out = gr.Textbox(label="Random Fact")

    def on_submit(name, topic):
        logger.info(f"User submitted: name='{name}', topic='{topic}'")
        return greet_haiku_fact(name, topic)

    submit_btn.click(on_submit, inputs=[name, topic], outputs=[greeting_out, haiku_out, fact_out])
    name.submit(on_submit, inputs=[name, topic], outputs=[greeting_out, haiku_out, fact_out])
    topic.submit(on_submit, inputs=[name, topic], outputs=[greeting_out, haiku_out, fact_out])

# Mount Gradio at a subpath, e.g., "/ui"
logger.info("Mounting Gradio app at /ui")
app = gr.mount_gradio_app(app, demo, path="/ui")

@app.get("/manifest.json")
def manifest():
    logger.debug("Serving manifest.json")
    return JSONResponse({
        "name": "Snack Facts Generator",
        "short_name": "SnackFacts",
        "start_url": "/ui",
        "display": "standalone",
        "background_color": "#ffffff",
        "description": "A Gradio app for snack facts as haikus."
    })