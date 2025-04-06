Reset Password
==============

This section contains endpoints for requesting a password reset and resetting the password using a token.

.. http:post:: /forgot-password/

   Request password reset.

   :query email: User's email address

   :status 200: Reset email sent successfully
   :status 404: User not found

   **Example Request:**
   .. code-block:: http

      POST /forgot-password/?email=user@example.com

   **Example Response:**
   .. code-block:: json

      {
         "message": "Password reset email sent. Please check your email."
      }

.. http:post:: /reset-password/{token}

   Reset password using token.

   :param token: Password reset token from email
   :query new_password: New password

   :status 200: Password reset successfully
   :status 400: Invalid or expired token
   :status 404: User not found

   **Example Request:**
   .. code-block:: http

      POST /reset-password/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...?new_password=newsecretpassword

   **Example Response:**
   .. code-block:: json

      {
         "message": "Password has been reset successfully"
      }

Notes
-----

- Ensure the `email` parameter is a valid registered email address when requesting a password reset.
- The `token` used for resetting the password must be valid and not expired.
- If the token is invalid or expired, the user will need to request a new password reset email.


