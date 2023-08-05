import setuptools

long_desc = open("README.md").read()
required = ['numpy'] # Comma seperated dependent libraries name

setuptools.setup(
    name="pyandavar",
    version="0.0.1", # eg:1.0.0
    author="rohith",
    author_email="ndrohith09@gmail.com",
    license="MIT",
    description="description of your package",
    long_description='long description of your package',
    long_description_content_type="text/markdown",
    url="https://github.com/ndrohith09/simple_todo_django",
    packages = ['src'],
    key_words="test",
    install_requires=required,
    # packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)