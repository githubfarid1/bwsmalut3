import os
import environ
from os.path import dirname, abspath, join
BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DBNAME =  os.getenv('DB_NAME')
PORT = os.getenv('DB_PORT')
USER = os.getenv('DB_USERNAME')
PASSWORD = os.getenv('DB_PASS')

DEPARTMENT_TABLE = "department"
BUNDLE_TABLE = "bundle"
DOC_TABLE = "doc"
TABLE_PREFIX = "arsip_inaktif_"
APP_NAME = "arsip_inaktif"
COVER_LOCATION = os.path.join("/home/arsip1/dev/bwsmalut3/apps", "static", "cover")
PDF_LOCATION = "/home/farid/pdfs/"
EXCEL_FILE = "/home/arsip1/dev/bwsmalut3/utilities/data/Daftar Arsip-asli.xlsx"
EXCEL_SHEET = ["IRIGASI", "AIR BAKU", "PANTAI", "SUNGAI", "KEUANGAN"]
# EXCEL_SHEET = ["KEUANGAN"]
TMPPDF_LOCATION = "/home/arsip1/dev/bwsmalut3/media/tmpfiles"

BACKUP_LOCATION = "/home/arsip1/backup"
