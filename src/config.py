from dotenv import load_dotenv
import os

load_dotenv()
marvel_public_key = os.environ.get("MARVEL_PUBLIC_KEY")
marvel_private_key = os.environ.get("MARVEL_PRIVATE_KEY")
