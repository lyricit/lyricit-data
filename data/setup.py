from setuptools import setup, find_packages

setup(
    name="lyricit",
    version="0.3",
    author="lyricit",
    author_email="your.email@example.com",
    description="A simple example package",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    packages=find_packages(where='src'),
    python_requires='>=3.6',
)