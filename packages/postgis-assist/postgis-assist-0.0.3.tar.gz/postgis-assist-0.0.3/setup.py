import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="postgis-assist",
    version="0.0.3",
    author="Aditya Kushwaha",
    author_email="kaditya9711@gmail.com",
    description="Package for Postgis query using python",
    py_modules=['postgis'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kaditya97/postgis-assist",
    packages=['postgis'],
    keywords=['postgresql', 'postgres', 'database',
              'sql', 'api', 'table', 'pg', 'postGIS'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['psycopg2'],
    python_requires='>=3.6',
)
