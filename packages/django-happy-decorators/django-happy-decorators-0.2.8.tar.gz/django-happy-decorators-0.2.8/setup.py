#!/usr/bin/env python

if __name__ == "__main__":
    import setuptools
    setuptools.setup(
        name="django-happy-decorators",
        version="0.2.8",
        author="Hatim Makki Hoho",
        author_email="hatim.makki@gmail.com",
        description="Django Happy Decorators - a collection of helper decorators for Django",
        url="https://github.com/hatimmakki/django-happy-decorators",
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )
