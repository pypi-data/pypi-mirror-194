from io import BytesIO
import base64
def image_b64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_str = base64.b64encode(buffered.getvalue())
    return image_str