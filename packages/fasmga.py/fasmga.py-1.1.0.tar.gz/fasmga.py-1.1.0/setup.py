import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fasmga.py",
    version="1.1.0",
    author="Vincy.zsh",
    author_email="Vincysuper07@gmail.com",
    description="A Fasm.ga API wrapper written using asyncio.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vincydotzsh/fasmga.py",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohttp"],
    packages=["fasmga"],
    python_requires=">=3.7",
)