# Data Samanvayah Agent (DSA)

Data Samanvayah Agent is a Python-based, multi-agent data science workflow built with LangGraph. The workflow coordinates memory, data-quality, planning, exploration, training, and critic agents through a shared `DSAState`.

The repository contains two ways to use DSA:

- **CLI:** runs the real LangGraph workflow against a local dataset.
- **Terminal UI:** `ui/dsa-terminal-ui.html` is a static, CRT-style product demo. It runs entirely in the browser and simulates a pipeline run; it is not connected to the Python CLI or a web API.

## Requirements

- Python 3.10 or newer
- pip, or [uv](https://docs.astral.sh/uv/)
- An OpenAI API key for agents that use an OpenAI model

The included `data/sample.csv` is suitable for verifying the installation. For a real run, provide a CSV or another dataset supported by the configured agents.

## Installation

### Windows PowerShell

```powershell
git clone https://github.com/devsripathy/Data-Samanvayah-Agent.git
Set-Location Data-Samanvayah-Agent

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` and activate again. Activation is optional after installation; commands can also be run with `.venv\Scripts\python.exe`.

### macOS/Linux

```bash
git clone https://github.com/devsripathy/Data-Samanvayah-Agent.git
cd Data-Samanvayah-Agent

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Using uv

```bash
uv venv
uv pip install -e ".[dev]"
```

The optional observability dependencies can be installed with:

```bash
python -m pip install -e ".[observability]"
```

## Configuration

DSA works with the defaults in `src/core/config.py`. To configure an LLM or optional observability, create a `.env` file in the repository root:

```env
LLM__PROVIDER=openai
LLM__MODEL=gpt-4o
LLM__API_KEY=your-openai-api-key
LLM__TEMPERATURE=0.2
LLM__MAX_TOKENS=4096

OBSERVABILITY__LANGSMITH_ENABLED=false
OBSERVABILITY__LANGSMITH_API_KEY=your-langsmith-key
OBSERVABILITY__LANGSMITH_PROJECT=dsa-agent

LOGGING__LEVEL=INFO
```

Environment variables use the nested `SECTION__FIELD` format. A `config.yaml` file is also supported for non-secret settings. Do not commit `.env`, API keys, generated checkpoints, or model artifacts.

## Run the CLI

After installation, the console script and the module entry point are equivalent:

```bash
# Run the sample dataset
dsa run data/sample.csv

# The same command without the installed console script
python main.py run data/sample.csv
```

Useful options:

```bash
# Use a stable session ID so it can be inspected or resumed
dsa run data/sample.csv --session-id demo_session

# Enable human-in-the-loop behavior
dsa run data/sample.csv --enable-hitl

# Persist LangGraph checkpoints to SQLite
dsa run data/sample.csv --session-id sqlite_run --sqlite
```

Session commands:

```bash
dsa list-sessions
dsa status demo_session
dsa resume demo_session
dsa resume demo_session --dataset data/sample.csv
```

Session JSON files are written to `data/sessions/`. When `--sqlite` is used, checkpoint databases are written to `data/checkpoints/`. These generated directories are local runtime state and should not be committed.

## Open the terminal UI

The UI is a static HTML demo and does not require Python dependencies or an API key. Open `ui/dsa-terminal-ui.html` directly in a browser, or serve the `ui` directory locally:

```bash
python -m http.server 8080 --directory ui
```

Then open <http://localhost:8080/dsa-terminal-ui.html>. Use **F1-F5** or the navigation buttons to switch views, select a dataset, and press **EXECUTE** to watch the simulated pipeline and critic output.

## Development

Run the test suite:

```bash
python -m pytest -q
```

Run the available checks:

```bash
ruff check src tests
mypy src --ignore-missing-imports
```

The main workflow is assembled in `src/core/graph.py`; shared state is defined in `src/core/state.py`; agent nodes live under `src/agents/`.

## Docker

Build the CLI image:

```bash
docker build -t dsa-agent .
```

Run it with a local dataset and optional environment file:

```bash
docker run --rm --env-file .env `
  -v "${PWD}/data:/app/data" `
  dsa-agent run data/sample.csv
```

On macOS/Linux, use `\` instead of PowerShell's backtick for line continuation. The Docker image is configured for the Python CLI; serve the static UI from the host with the `http.server` command above.

## Project layout

```text
src/
  agents/       Specialized LangGraph nodes
  core/         Graph, state, configuration, and observability
  cli/          Lightweight Typer CLI entry point
data/           Sample data and local session examples
tests/          Pytest tests
ui/             Static terminal UI demo
main.py         Full session-aware CLI entry point
```
