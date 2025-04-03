def test_create_contact(client, test_user_token):
    """
    Test the creation of a new contact using the API.

    This test verifies that a contact can be successfully created by sending
    a POST request to the `/contacts/` endpoint with valid contact data and
    an authorization token. It checks the following:

    1. The response status code is 200, indicating a successful operation.
    2. The response JSON contains the correct contact details as provided in the request.
    3. The response JSON includes an "id" field, confirming that the contact was created
       and assigned a unique identifier.

    Args:
        client (TestClient): The test client used to simulate API requests.
        test_user_token (str): A valid JWT token for authenticating the request.

    Raises:
        AssertionError: If any of the assertions fail, indicating that the contact
                        creation did not behave as expected.
    """
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "1234567890",
        "birthday": "1990-01-01",
        "additional_info": "Test contact",
    }
    response = client.post(
        "/contacts/",
        headers={"Authorization": f"Bearer {test_user_token}"},
        json=contact_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == contact_data["first_name"]
    assert data["last_name"] == contact_data["last_name"]
    assert data["email"] == contact_data["email"]
    assert "id" in data
