from io import BytesIO
import base64
from PIL import Image
def image_b64(file):
    image = Image.open(file)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_str = base64.b64encode(buffered.getvalue())
    return image_str