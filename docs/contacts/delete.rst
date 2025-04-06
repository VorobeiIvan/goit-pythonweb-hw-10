Delete Contact
==============

This endpoint allows the user to delete a specific contact by providing the contact ID.

.. http:delete:: /contacts/{contact_id}

   Delete a contact.

   :header Authorization: Bearer {token}
   :param contact_id: Contact ID

   :status 200: Contact deleted successfully
   :status 401: Not authenticated
   :status 403: Forbidden (if the user does not have access to the contact)
   :status 404: Contact not found

   **Example Request:**
   .. code-block:: http

      DELETE /contacts/1
      Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

   **Example Response:**
   .. code-block:: json

      {
         "message": "Contact deleted successfully"
      }

Notes
-----

- The `Authorization` header must contain a valid Bearer token.
- Ensure the user has access to the contact before attempting to delete it.
