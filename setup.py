import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-daterangefilter",
    version="0.0.1",
    license='MIT',
    author="Andrey Novikov",
    author_email="novikov@gmail.com",
    description="Date range filter for Django admin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andreynovikov/django-daterangefilter/tree/master",
    packages=setuptools.find_packages(),
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
