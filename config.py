from os import getenv

PORT      = int(getenv("PORT")) or 8080
MONGO_URI = getenv("MONGO_URI")
