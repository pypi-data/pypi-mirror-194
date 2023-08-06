import setuptools

setuptools.setup(
    name="backloader",
    version="1.0.0",
    author="Aiden Kundert",
    author_email="aidenkundert060@gmail.com",
    description="If you have something that requires importing lots of packages (5,000): baS.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://replit.com/@-jpg/backloader#setup.py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)