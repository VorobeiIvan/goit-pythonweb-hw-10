Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api
   database
   models
   main
   testing
   auth/reset-password
   auth/verify
   auth/avatar
   contacts/create
   contacts/read
   contacts/update
   contacts/delete
   users/profile

Installation
------------

To get started with the FastAPI Contacts API, follow these steps:

1. Clone the repository:

   .. code-block:: bash

      git clone https://github.com/yourusername/fastapi-contacts-api.git
      cd fastapi-contacts-api

2. Create a virtual environment:

   .. code-block:: bash

      python -m venv venv
      source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:

   .. code-block:: bash

      pip install -r requirements.txt

4. Run the application:

   .. code-block:: bash

      uvicorn main:app --reload


