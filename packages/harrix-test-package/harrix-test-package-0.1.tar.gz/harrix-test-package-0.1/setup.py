from setuptools import find_packages, setup
import pathlib
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="harrix-test-package",
    version="0.1",
    description="Test package",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Harrix/harrix-test-package",
    author="Anton Sergienko",
    author_email="anton.b.sergienko@gmail.com",
    install_requires=[],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)