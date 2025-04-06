Register User
=============

This endpoint allows a new user to register by providing their email and password.

.. http:post:: /api/auth/register

   Register a new user.

   **Request Body**

   .. code-block:: json

      {
         "email": "user@example.com",
         "password": "string"
      }

   **Response**

   .. code-block:: json

      {
         "email": "user@example.com",
         "id": 1,
         "is_active": true,
         "is_verified": false,
         "created_at": "2024-03-20T10:00:00",
         "updated_at": "2024-03-20T10:00:00"
      }

   :statuscode 201: User successfully created
   :statuscode 400: Email already registered
   :statuscode 422: Validation Error

Notes
-----

- The `email` field must be unique and in a valid email format.
- The `password` field must meet the application's password complexity requirements.
- If the email is already registered, the API will return a `400` status code.


