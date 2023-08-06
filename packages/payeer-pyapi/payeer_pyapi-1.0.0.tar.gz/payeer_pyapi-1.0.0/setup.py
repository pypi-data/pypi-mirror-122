import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="payeer_pyapi",

    version="1.0.0",

    author="Mr Storm",
    author_email="medikk19@mail.ru",

    description="Connecting the Payeer payment system to your product",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/St0rm1k/payeer_pyapi",

    project_urls={
        "GitHub": "https://github.com/St0rm1k/payeer_pyapi",
        "Guide": "https://github.com/St0rm1k/payeer_pyapi/blob/main/README.md",
        "Bug Tracker": "https://github.com/St0rm1k/payeer_pyapi/issues",
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=["payeer_pyapi"],
    install_requires=["requests"],
    python_requires=">=3.7",
)
