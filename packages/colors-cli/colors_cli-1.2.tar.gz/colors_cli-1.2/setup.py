from setuptools import setup
from pathlib import Path

this_dir = Path(__file__).parent
long_description = (this_dir / "README.md").read_text()

setup(
    name="colors_cli",
    version="1.2",
    description="Backlight color for command line interface!",
    packages=["src"],
    author_email="dimf29@gmail.com",
    author="sobraniebluee",
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
