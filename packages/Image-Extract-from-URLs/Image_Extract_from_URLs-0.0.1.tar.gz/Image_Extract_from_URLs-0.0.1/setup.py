from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='Image_Extract_from_URLs',
    version='0.0.1',
    author="Suriyakrishnan Sathish",
    description="Downloading Images from the URLs in the txt file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['image_extract_from_urls'],
    entry_points={
        'console_scripts': [
            'image_extract_from_urls = image_extract_from_urls.__main__:main'
        ]
    })
