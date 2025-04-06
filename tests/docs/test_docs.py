import os
import subprocess
import pytest


DOCS_PATH = "docs"
BUILD_PATH = os.path.join(DOCS_PATH, "_build")
HTML_PATH = os.path.join(BUILD_PATH, "html")


@pytest.fixture(scope="module")
def build_docs():
    """
    Build the Sphinx documentation before running tests.
    """
    if os.path.exists(BUILD_PATH):
        subprocess.run(["rm", "-rf", BUILD_PATH], check=True)
    result = subprocess.run(
        ["make", "html"], cwd=DOCS_PATH, capture_output=True, text=True
    )
    if result.returncode != 0:
        pytest.fail(f"Failed to build documentation: {result.stderr}")
    yield
    # Clean up after tests
    subprocess.run(["rm", "-rf", BUILD_PATH], check=True)


def test_docs_build_success(build_docs):
    """
    Test that the documentation builds successfully.
    """
    assert os.path.exists(HTML_PATH), "HTML documentation was not generated."


def test_index_page_exists(build_docs):
    """
    Test that the index.html page exists in the generated documentation.
    """
    index_path = os.path.join(HTML_PATH, "index.html")
    assert os.path.exists(
        index_path
    ), "index.html is missing in the generated documentation."


def test_no_warnings_in_build(build_docs):
    """
    Test that there are no warnings during the documentation build.
    """
    result = subprocess.run(
        ["make", "html"], cwd=DOCS_PATH, capture_output=True, text=True
    )
    assert "WARNING" not in result.stderr, "Warnings found during documentation build."
