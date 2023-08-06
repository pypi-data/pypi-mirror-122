import setuptools

VERSION = '0.1.22'
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

# Setting up
setuptools.setup(
    name="HALdata",
    version=VERSION,
    author="Cole Crescas",
    author_email="<colecrescas@gmail.com>",
    description="Transfering Data between s3, snowflake & Domo with server integration",
    long_description = long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/colaso96/HALdata',
    install_requires=['pandas', 'numpy', 'json', 'botocore', 'snowflake.connector', 'boto3'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',
)