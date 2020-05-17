import os

# Grabs the folder where the script runs.
project_dir = os.path.dirname(os.path.abspath(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
database_filename = "database.db"
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

# IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = database_path

SQLALCHEMY_TRACK_MODIFICATIONS = False
