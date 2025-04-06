Verify Email
============

This endpoint verifies the user's email address using a token sent to their email.

.. http:get:: /verify/{token}

   Verify user's email address.

   :param token: Verification token from email

   :status 200: Email verified successfully
   :status 400: Invalid token
   :status 401: Unauthorized (if the token is expired or invalid)
   :status 404: User not found

   **Example Request:**
   .. code-block:: http

      GET /verify/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

   **Example Response:**
   .. code-block:: json

      {
         "message": "Email verified successfully"
      }

Notes
-----

- The verification token must be valid and not expired.
- If the token is invalid or expired, the user will need to request a new verification email.


