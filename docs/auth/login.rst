Login User
==========

This endpoint allows a user to log in by providing their email and password. Upon successful authentication, an access token is returned.

.. http:post:: /api/auth/login

   Login user with email and password.

   **Request Body**

   .. code-block:: json

      {
         "email": "user@example.com",
         "password": "string"
      }

   **Response**

   .. code-block:: json

      {
         "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
         "token_type": "bearer"
      }

   :statuscode 200: Successfully logged in
   :statuscode 401: Invalid credentials
   :statuscode 403: Forbidden (if the user account is locked)
   :statuscode 422: Validation Error

Notes
-----

- The `email` and `password` fields are required in the request body.
- The returned `access_token` should be included in the `Authorization` header for subsequent requests.
- If the user account is locked or inactive, the API may return a `403 Forbidden` status code.

