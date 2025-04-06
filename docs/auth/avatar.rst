User Avatar
===========

This endpoint allows an admin user to update the avatar of a user by uploading an image file.

.. http:put:: /users/avatar/

   Update user's avatar (admin only).

   :header Authorization: Bearer {token}
   :form file: Avatar image file (multipart/form-data)

   :status 200: Avatar updated successfully
   :status 401: Not authenticated
   :status 403: Forbidden (if the user does not have admin privileges)
   :status 422: Validation Error

   **Example Request:**
   .. code-block:: http

      PUT /users/avatar/
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
      Content-Type: multipart/form-data

      --boundary
      Content-Disposition: form-data; name="file"; filename="avatar.jpg"
      Content-Type: image/jpeg

      [binary data]
      --boundary--

   **Example Response:**
   .. code-block:: json

      {
         "message": "Avatar updated successfully",
         "avatar_url": "https://example.com/uploads/avatar.jpg"
      }

Notes
-----

- The `Authorization` header must contain a valid Bearer token.
- Only users with admin privileges can update avatars.
- The uploaded file must be in a valid image format (e.g., JPEG, PNG).
