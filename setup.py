import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="trello_client-basics-api-DenKarlos",
    version="0.0.1", author="Kominarets Denis",
    author_email="kominaretsdenis@yandex.ru",
    description="Programm that from python script interact with Trello using API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DenKarlos/Trello_console_client",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3",
                 "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ],
    python_requires='>=3.6',)
