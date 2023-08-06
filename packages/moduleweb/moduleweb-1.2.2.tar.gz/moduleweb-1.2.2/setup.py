from setuptools import setup, find_packages

# with open("README.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
    name="moduleweb",
    version="1.2.2",
    author = "Egor Machnev",
    author_email = "egorikhelp@gmail.com",
    keywords = "python library framework web async aiohttp moduleweb",
    description = "A simple, intuitive and user-friendly library based on Aiohttp, written for faster and more convenient web development in Python🎍",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/machnevegor/moduleweb",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    install_requires=["aiohttp", "jinja2", "aiohttp_jinja2", "attr"],
    python_requires=">=3.7"
)
