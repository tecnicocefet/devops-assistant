import os

# ===== Projeto =====

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ===== Caminhos =====

DATA_DIR = os.path.join(BASE_DIR, "data")
LABS_DIR = os.path.join(BASE_DIR, "labs")
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge-base")
ANALYSIS_DIR = os.path.join(BASE_DIR, "analysis")


# ===== Modelos =====

DEFAULT_MODEL = "deepseek-coder:6.7b"


# ===== Ollama =====

OLLAMA_HOST = "http://localhost:11434"