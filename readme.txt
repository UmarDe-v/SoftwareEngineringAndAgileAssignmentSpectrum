Software Engineering & Agile — Python FastAPI PostgreSQL Project

Overview
--------
This is a Python web application built using the FastAPI framework and PostgreSQL as the database.
The system supports user authentication, admin access, and license management features.
The codebase follows a modular structure with clearly separated routes, models, and utility files located inside the app/ directory.

Prerequisites (tested and working on)
-------------------------------------
- Python 3.12.10
- PostgreSQL 17.x installed and running

Setup and Installation
----------------------
1. Download the project folder.

2. Ensure PostgreSQL is installed and running.
   To verify, open Command Prompt and run:
   psql --version

   If you get an error like 'psql' is not recognized, it means PostgreSQL’s bin folder is not in your system PATH.
   Add it to your PATH environment variable. The typical path looks like:

   C:\Program Files\PostgreSQL\17\bin

3. Import the provided SQL dump file into your PostgreSQL database using pgAdmin4 or your preferred system.
   Example using the command line:
   psql -U your_db_username -d your_database_name -f "spectrum_backup_database.sql"

   If your database is named `test_db`, the command might look like:
   psql -U postgres -d test_db -f "C:\Users\umr\Desktop\Uni assignment\spectrum_backup_database.sql"

4. Create and activate a Python virtual environment (recommended):

   On Windows:
   python -m venv test_env  
   test_env\Scripts\activate.bat

5. Install required Python packages on the VM:
   pip install -r requirements.txt

6. Run the application:
   python main.py

Configuration
-------------
- Edit the database URL directly in the file `app/db.py`, for example:
  SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/test_db"

Running the Application
-----------------------
- Make sure your virtual environment is activated and PostgreSQL server is running.
- Then run:
  python main.py

- By default, FastAPI will be available at (swagger):
  http://127.0.0.1:8000/docs

Notes
-----
- `psycopg2-binary` is used for PostgreSQL connection and is included in `requirements.txt`.
- No `.env` file or GitHub repository setup is required.
- SQL schema is provided in `spectrum_backup_database.sql`.
- Tested on: Python 3.12.10, PostgreSQL 17.4

Troubleshooting
---------------
- If you get psycopg2 or DLL errors, make sure `psycopg2-binary` is installed inside your virtual environment.
- Ensure PostgreSQL is running and credentials in `app/db.py` are correct.
- If psql is not recognized, ensure PostgreSQL’s bin folder is in your system PATH.

---

Thank you - Umar S
