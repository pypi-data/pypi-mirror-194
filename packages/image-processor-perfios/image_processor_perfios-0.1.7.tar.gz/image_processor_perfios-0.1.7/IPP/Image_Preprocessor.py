from torchvision import transforms
import numpy as np

def image_mnist(image):
    # Load the image and preprocess it
    img = image.convert('L').resize((28, 28))

    # Convert the image to a tensor
    transform = transforms.Compose([transforms.ToTensor()]) 
    tensor = transform(img)

    # Normalize the tensor
    mean, std = (0.1307,), (0.3081,) # MNIST dataset mean and std
    tensor = transforms.Normalize(mean=mean, std=std)(tensor)

    # Add a batch dimension to the tensor and pass it through the model
    tensor = tensor.unsqueeze(0)
    return tensor

