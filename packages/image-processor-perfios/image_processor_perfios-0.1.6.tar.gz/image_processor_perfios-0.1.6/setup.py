from setuptools import setup, find_packages

setup(
    name="image_processor_perfios",
    version="0.1.6",
    author="Nandana K A",
    author_email="ext-nandana.ka@perfios.com",
    description="A module to pre-process,infer and postprocess an image",
    packages=find_packages(),
    install_requires=["Pillow","torch","torchvision","numpy"],
)