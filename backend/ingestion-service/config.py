# Create the config.py file that main.py is looking for
@"
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_CONN_STRING = os.getenv("DB_CONN_STRING", "host=postgis user=postgres password=postgres dbname=terrapulse sslmode=disable")
    NASA_API_KEY = os.getenv("NASA_API_KEY", "your_nasa_api_key_here")
    # You can add other settings as needed

settings = Settings()
"@ | Out-File -FilePath ./backend/ingestion-service/config.py -Encoding utf8"