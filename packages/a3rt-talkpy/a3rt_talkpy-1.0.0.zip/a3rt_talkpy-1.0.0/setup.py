import setuptools
import a3rt_talkpy

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=a3rt_talkpy.__name__,
    version=a3rt_talkpy.__version__,
    author=a3rt_talkpy.__author__,
    description=a3rt_talkpy.__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=a3rt_talkpy.__url__,
    packages=setuptools.find_packages(),
    classifiers=a3rt_talkpy.__classifiers__,
)
