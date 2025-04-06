import os


HTML_PATH = "docs/_build/html"


def test_api_section_exists():
    """
    Test that the API section exists in the generated documentation.
    """
    api_path = os.path.join(HTML_PATH, "api.html")
    assert os.path.exists(api_path), "API section is missing in the documentation."


def test_auth_section_exists():
    """
    Test that the Authentication section exists in the generated documentation.
    """
    auth_path = os.path.join(HTML_PATH, "auth/login.html")
    assert os.path.exists(
        auth_path
    ), "Authentication section is missing in the documentation."


def test_contacts_section_exists():
    """
    Test that the Contacts section exists in the generated documentation.
    """
    contacts_path = os.path.join(HTML_PATH, "contacts/create.html")
    assert os.path.exists(
        contacts_path
    ), "Contacts section is missing in the documentation."
