from setuptools import setup, find_packages

setup(
    name='django-metanotes',
    version='0.1.0-dev',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=3.0',
    ],
    author="Milan Slesarik",
    author_email="milslesarik@gmail.com",
    description="A Django app for adding developer notes to pages.",
    url="https://github.com/milsl/django-metanotes",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 2 - Pre-Alpha",
    ],
)
