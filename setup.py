import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django-daterangefilter',
    version='0.2.0',
    license='MIT',
    author='Andrey Novikov',
    author_email='novikov@gmail.com',
    description='Date range filter for Django admin',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/andreynovikov/django-daterangefilter/tree/master',
    project_urls={
        'Source': 'https://github.com/andreynovikov/django-daterangefilter/',
        'Tracker': 'https://github.com/andreynovikov/django-daterangefilter/issues',
    },
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
