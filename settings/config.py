import os
ENV = "DEV"  #<--- change here DEV or PROD
## keys
if ENV == "DEV":
 from settings import keys
 telegram_key = keys.telegram_key
 mongodb_key = keys.mongodb_key
elif ENV == "PROD":
 import ast
 telegram_key = ast.literal_eval(os.environ["telegram_key"])
 mongodb_key = ast.literal_eval(os.environ["mongodb_key"])
## server
host = "0.0.0.0"
port = int(os.environ.get("PORT", 5000))