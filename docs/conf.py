import os
import sys

# Додаємо шлях до кореневої папки проекту
sys.path.insert(0, os.path.abspath("../"))

# Додаємо шлях до папки `app`
sys.path.insert(0, os.path.abspath("../app"))

project = "FastAPI Contacts API"
copyright = "2025, Ivan Vorobei"
author = "Ivan Vorobei"

release = "1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
    "sphinxcontrib.httpdomain",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"
