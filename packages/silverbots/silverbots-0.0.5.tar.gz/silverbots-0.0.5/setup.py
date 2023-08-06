import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="silverbots",
    version="0.0.5",
    author="SrJSilver",
    author_email="Sergey081203@ya.ru",
    description="Silver Bots",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WwWSrJSilverWwW/SilverBots",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
