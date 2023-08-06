import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="anonupload",
    version="1.0.1",
    author="Jak Bin",
    description="file upload to anonfile server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakbin/anonfile-upload",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='anonfile,anonymous,upload',

    packages=["anonupload"],

    entry_points={
        "console_scripts":[
            "anon = anonupload:main"
        ]
    }
)
