import pytest
from jose import jwt
from app.services.auth import create_access_token, verify_password
from app.utils.security import pwd_context
from app.utils.dependencies import SECRET_KEY, ALGORITHM


# Test the creation of an access token
def test_create_access_token():
    # Define the payload data for the token
    data = {"sub": "test@example.com"}
    # Generate the access token using the create_access_token function
    token = create_access_token(data)
    # Decode the token to verify its contents
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # Assert that the "sub" field in the payload matches the input data
    assert payload.get("sub") == "test@example.com"


# Test the password verification functionality
def test_verify_password():
    # Define a plain text password
    plain_password = "testpassword123"
    # Hash the plain text password using the password hashing context
    hashed_password = pwd_context.hash(plain_password)
    # Verify that the plain password matches the hashed password
    assert verify_password(plain_password, hashed_password)
    # Verify that an incorrect password does not match the hashed password
    assert not verify_password("wrongpassword", hashed_password)


# Test the user registration endpoint
def test_register_user(client):
    # Send a POST request to the /auth/register/ endpoint with user details
    response = client.post(
        "/auth/register/",
        json={"email": "newuser@example.com", "password": "newpassword123"},
    )
    # Assert that the response status code is 200 (success)
    assert response.status_code == 200
    # Assert that the response contains a success message
    assert "User registered successfully" in response.json()["message"]


# Test registering a user with an email that already exists
def test_register_duplicate_user(client, test_user):
    # Send a POST request to the /auth/register/ endpoint with duplicate user details
    response = client.post(
        "/auth/register/",
        json={"email": test_user["email"], "password": "anotherpassword123"},
    )
    # Assert that the response status code is 400 (bad request)
    assert response.status_code == 400
    # Assert that the response contains an error message about the duplicate user
    assert "User already exists" in response.json()["detail"]


# Test successful login with valid credentials
def test_login_success(client, test_user):
    # Send a POST request to the /auth/token endpoint with valid credentials
    response = client.post(
        "/auth/token",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    # Assert that the response status code is 200 (success)
    assert response.status_code == 200
    # Assert that the response contains an access token
    assert "access_token" in response.json()
    # Assert that the token type is "bearer"
    assert response.json()["token_type"] == "bearer"


# Test login with invalid credentials
def test_login_invalid_credentials(client):
    # Send a POST request to the /auth/token endpoint with incorrect credentials
    response = client.post(
        "/auth/token",
        data={"username": "wrong@example.com", "password": "wrongpassword"},
    )
    # Assert that the response status code is 401 (unauthorized)
    assert response.status_code == 401
    # Assert that the response contains an error message about invalid credentials
    assert "Invalid credentials" in response.json()["detail"]
