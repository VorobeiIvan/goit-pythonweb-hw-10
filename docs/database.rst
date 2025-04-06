Database Configuration
======================

This module handles the database connection and configuration for the FastAPI Contacts API.

.. automodule:: database
   :members:
   :undoc-members:
   :show-inheritance:

Example Configuration
---------------------

.. code-block:: python

   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker

   DATABASE_URL = "postgresql://user:password@localhost/dbname"

   engine = create_engine(DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   