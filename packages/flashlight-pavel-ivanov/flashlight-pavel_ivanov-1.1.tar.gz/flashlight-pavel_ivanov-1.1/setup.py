import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="flashlight-pavel_ivanov",
    version="1.1",
    author="Pavel Ivanov",
    author_email="pavel@ivanov928.ru",
    description="This is a package with interview test.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Splinter928/flashlight",
    packages=['flashlight'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)