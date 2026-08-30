from dotenv import load_dotenv
import os

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
access_token_expire_minitues = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))