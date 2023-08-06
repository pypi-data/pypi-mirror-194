import torch
def image_detect_digit(image_tensor,model):
    output = model(image_tensor)
    return torch.argmax(output,dim=None).item()

