import setuptools

with open("docs/pypi.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='deeploy',
    version='0.3.0',
    description='The official Deeploy client for Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Lars Suanet',
    author_email='lars@deeploy.ml',
    packages=setuptools.find_packages(),
    url="https://gitlab.com/deeploy-ml/deeploy-python-client",
    project_urls={
        "Documentation": "https://deeploy-ml.gitlab.io/deeploy-python-client/",
        "Deeploy website": "https://deeploy.ml",
    },
    install_requires=[
        "pydantic==1.8.2",
        "gitpython==3.1.23",
        "requests==2.26.0",
        "joblib>=1.0.1",
        "dill>=0.3.3",
        "ipython>=7.26.0",
        "nbconvert>=6.0.7",
        "torch-model-archiver==0.3.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
