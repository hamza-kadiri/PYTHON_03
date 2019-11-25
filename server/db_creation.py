import database
import sys
"""Script to erase the database and create a new one"""

if __name__ == "__main__":
    if "import" in sys.argv:
        import_data = True
    else:
        import_data = False
    database.initiation_db(import_data)
    print("DB Created")