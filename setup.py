from setuptools import setup


def readme():
    with open("README.md") as file:
        return file.read()


NAME = "latex-recognizer",


setup(
    name=NAME,
    version="1.0.0",
    description="Read the latest Real Python tutorials",
    long_description=readme(),
    long_description_content_type="text/markdown",
    # url="https://github.com/realpython/reader",
    author="CapBlood",
    author_email="stalker.anonim@mail.ru",
    license="GP",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    packages=["latex_recognizer"],
    include_package_data=True,
    install_requires=[
        "pyside2", "numpy",
        "qdarkstyle", "tensorflow",
        "opencv-python"
    ],
    entry_points={"console_scripts": ["latexrec=latex_recognizer.__main__:main"]},
)
