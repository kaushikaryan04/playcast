
import cloudinary
import cloudinary.api
import cloudinary.uploader

from dotenv import load_dotenv
import os

load_dotenv()


CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name= os.getenv("CLOUD_NAME"),
    api_key = os.getenv("API_KEY"),
    api_secret=CLOUDINARY_API_SECRET,
    secure=True,
)

def UploadFile(file ,**options) :
    cloudinary.uploader.upload(file) ;


def GetUrlOnSave(file ,**options) :
    response = cloudinary.uploader.upload(file, resource_type = "video")
    return response["secure_url"]
