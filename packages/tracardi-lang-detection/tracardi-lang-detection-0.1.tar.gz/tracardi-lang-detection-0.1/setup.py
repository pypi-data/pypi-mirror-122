from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tracardi-lang-detection',
    version='0.1',
    description='This plugin detects language from given string.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Bartlomiej Komendarczuk',
    author_email='bkomendarczuk@gmail.com',
    packages=['tracardi_lang_detection'],
    install_requires=[
        'tracardi-plugin-sdk',
        'tracardi'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords=['tracardi', 'plugin'],
    include_package_data=True,
    python_requires=">=3.8",
)