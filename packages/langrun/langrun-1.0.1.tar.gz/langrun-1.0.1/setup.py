import setuptools

setuptools.setup(
    name="langrun",
    version="1.0.1",
    author="zalo_halo",
    author_email="aidenkundert060@gmail.com",
    description="a simple package for running seperate languages in python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://replit.com/@-jpg/langrun",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)