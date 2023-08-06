from setuptools import setup
readme = open("./README.md", "r")
setup(
    name="name_sanitizer",
    packages=["ns"],
    version = "1.0.3",
    description = "Python script for sanitize files and directories names",
    long_description=readme.read(),
    long_description_content_type="text/markdown",
    author = "César Alejandro Mora Cid",
    author_email = "cesar.mcid@gmail.com",
    url="https://github.com/xcesaralejandro/name_sanitizer",
    download_url="https://github.com/xcesaralejandro/name_sanitizer",
    keywords=["name","sanitizer","directories","files"],
    python_requires=">=3.0",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    license="MIT",
    include_package_data=True
)
