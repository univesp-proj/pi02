import environ

from pi.settings.base import *

env = environ.Env()

DEBUG = env.bool ("DEBUG", False)
SECRET_KEY = env ("SECRET_KEY")
ALLOWED_HOSTS = env.list ("ALLOWED_HOSTS")
DATABASES = {
    "default": env.db(),
}

import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = env ("CLOUD_NAME"),
  api_key = env ("CLOUD_API_KEY"), 
  api_secret = env ("CLOUD_API_SECRET")
)
