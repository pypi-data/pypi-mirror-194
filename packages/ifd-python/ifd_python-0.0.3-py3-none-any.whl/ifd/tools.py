from .entities import Image
import json

def getDictFromBytes(data: bytes):
    data = data.decode("utf-8")
    return json.loads(data)
def getImageFromJson(json_image: str) -> Image:
    image: Image = Image()
    image.deserialize(json_image)
    return image
def getJsonFromImage(image: Image) -> str:
    return image.serialize()