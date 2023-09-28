"""File with settings and configs for the project."""
import os

from dotenv import load_dotenv

load_dotenv('.env')

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
