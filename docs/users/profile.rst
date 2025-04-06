User Profile
============

This endpoint retrieves the profile information of the currently authenticated user.

.. http:get:: /users/me

   Get current user's profile.

   :header Authorization: Bearer {token}

   :status 200: Success
   :status 401: Not authenticated
   :status 403: Forbidden (if the user does not have access)
   :status 404: Not found (if the user profile does not exist)

   **Example Request:**
   .. code-block:: http

      GET /users/me
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

   **Example Response:**
   .. code-block:: json

      {
         "id": 1,
         "email": "user@example.com",
         "is_active": true,
         "is_verified": true,
         "role": "admin",
         "avatar_url": "https://res.cloudinary.com/your-cloud-name/image/upload/v1234567890/avatar.jpg",
         "created_at": "2024-03-28T10:00:00",
         "updated_at": "2024-03-28T10:30:00"
      }

Notes
-----

- The `Authorization` header must contain a valid Bearer token.
- Ensure the user is authenticated before accessing this endpoint.

