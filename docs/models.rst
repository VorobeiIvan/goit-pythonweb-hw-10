Database Models
===============

User Model
----------

.. automodule:: models.user
   :members:
   :undoc-members:
   :show-inheritance:

Example User Model
------------------

.. code-block:: json

   {
      "id": 1,
      "email": "user@example.com",
      "is_verified": true,
      "created_at": "2025-04-06T12:00:00",
      "updated_at": "2025-04-06T12:30:00"
   }

Contact Model
-------------

.. automodule:: models.contacts
   :members:
   :undoc-members:
   :show-inheritance:

Example Contact Model
---------------------

.. code-block:: json

   {
      "id": 1,
      "first_name": "John",
      "last_name": "Doe",
      "email": "john.doe@example.com",
      "phone": "+123456789",
      "birthday": "1990-01-01",
      "additional_info": "Friend from work"
   }
