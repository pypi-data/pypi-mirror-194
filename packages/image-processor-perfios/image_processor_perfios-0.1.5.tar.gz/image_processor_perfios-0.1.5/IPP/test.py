from Image_Preprocessor import image_mnist
from Image_Inference import image_detect_digit

image_mnist = image_mnist('images/img_113.jpg')
output = image_detect_digit(image_mnist)
print(output)


