import os
import environ
from os.path import dirname, abspath, join
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DBNAME =  os.getenv('DB_NAME')
PORT = os.getenv('DB_PORT')
USER = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASS')

VARIETY_TABLE = "variety"
DOC_TABLE = "doc"
TABLE_PREFIX = "alihmedia_vital_"
APP_NAME = "alihmedia_vital"
PDF_LOCATION = "/home/farid/pdfs/"
EXCEL_FILE = "Contoh Daftar Arsip Vital_6 April 2023.xlsx"
