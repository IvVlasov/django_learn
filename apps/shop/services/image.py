import uuid
from PIL import Image
from django.core.files.images import ImageFile
from django.db.models.fields.files import ImageFieldFile
from io import BytesIO
import requests


def resize_image(image: ImageFieldFile | BytesIO) -> ImageFile:
    img = Image.open(image)
    width, heigth = img.size

    if width > heigth:
        white_color = (255, 255, 255, 255)
        background = Image.new("RGB", (width, width), color=white_color)
        y = width // 2 - heigth // 2
        x = 0
    else:
        white_color = (255, 255, 255, 255)
        background = Image.new("RGB", (heigth, heigth), color=white_color)
        x = heigth // 2 - width // 2
        y = 0
    background.paste(img, (x, y))
    filename = "%s.%s" % (uuid.uuid4(), "webp")
    output = BytesIO()
    background.save(fp=output, format="WEBP")
    img_object = ImageFile(BytesIO(output.getvalue()), name=filename)
    return img_object


def load_photo(url: str) -> BytesIO:
    r = requests.get(url, stream=True)
    bio = BytesIO(r.content)
    return bio
