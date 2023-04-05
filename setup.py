import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-daterangefilter',
    version='1.0.0',
    license='MIT',
    author='Andrey Novikov',
    author_email='novikov@gmail.com',
    description='Date range filter for Django admin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andreynovikov/django-daterangefilter/tree/master',
    project_urls={
        'Source': 'https://github.com/andreynovikov/django-daterangefilter/',
        'Tracker': 'https://github.com/andreynovikov/django-daterangefilter/issues'
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
