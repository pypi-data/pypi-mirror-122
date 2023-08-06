import ast
import io
import re

from setuptools import find_packages, setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r"description\s+=\s+(?P<description>.*)")

with open("lektor_gemini_capsule.py", "rb") as f:
    description = str(
        ast.literal_eval(_description_re.search(f.read().decode("utf-8")).group(1))
    )

setup(
    author="Evilham",
    author_email="cvs@evilham.com",
    description=description,
    keywords="Lektor plugin",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="lektor-gemini-capsule",
    packages=find_packages(),
    py_modules=["lektor_gemini_capsule"],
    url="https://git.sr.ht/~evilham/lektor-gemini-capsule",
    version="0.1",
    classifiers=[
        "Framework :: Lektor",
        "Environment :: Web Environment",
        "Environment :: Plugins",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "lektor.plugins": [
            "gemini-capsule = lektor_gemini_capsule:GeminiCapsulePlugin",
        ]
    },
)
