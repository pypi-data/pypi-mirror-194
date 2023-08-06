from setuptools import setup, find_packages

setup(
    name="image_processor_perfios",
    version="0.1.8",
    author="Nandana K A",
    author_email="ext-nandana.ka@perfios.com",
    description="A module to pre-process,infer and postprocess an image",
    packages=find_packages(),
    install_requires=["Pillow>=9.4.0","torch>=1.10.0","torchvision>=0.14.1","numpy>=1.24.2"],
)