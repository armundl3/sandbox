import typer
import subprocess
import os
import requests

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

def check_ollama():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        if r.status_code == 200:
            return True
    except Exception:
        pass
    typer.secho("Ollama is not running at {}. Please start Ollama (e.g., run 'ollama serve') before launching the app.".format(OLLAMA_URL), fg=typer.colors.RED, err=True)
    raise typer.Exit(code=1)

app = typer.Typer()

@app.command()
def run_local(model: str = typer.Option("mistral", help="Ollama model to use (e.g., mistral, llama3, phi3)")):
    """Run the app locally using Poetry."""
    check_ollama()
    os.environ["OLLAMA_MODEL"] = model
    subprocess.run(["poetry", "run", "uvicorn", "play_cursor.main:app", "--reload"])

@app.command()
def run_docker(
    model: str = typer.Option("mistral", help="Ollama model to use (e.g., mistral, llama3, phi3)"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run container in detached mode")
):
    """Build and run the app using Docker."""
    check_ollama()
    subprocess.run(["docker", "build", "-t", "play-cursor", "."])
    run_cmd = [
        "docker", "run", "-e", f"OLLAMA_MODEL={model}", "-p", "8000:8000", "play-cursor"
    ]
    if detach:
        run_cmd.insert(2, "-d")
    subprocess.run(run_cmd)

@app.command()
def run_compose(
    model: str = typer.Option("mistral", help="Ollama model to use (e.g., mistral, llama3, phi3)"),
    detach: bool = typer.Option(False, "--detach", "-d", help="Run containers in detached mode")
):
    """Build and run the app using Docker Compose."""
    check_ollama()
    cmd = [
        "docker-compose", "up", "--build", "--remove-orphans"
    ]
    if detach:
        cmd.append("-d")
    subprocess.run(cmd)
    print(f"If you want to change the model, set OLLAMA_MODEL in your docker-compose.yml or override with: docker-compose run -e OLLAMA_MODEL={model} app")

if __name__ == "__main__":
    app() 