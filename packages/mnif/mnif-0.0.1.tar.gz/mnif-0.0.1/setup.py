import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mnif",
    version="0.0.1",
    author="Blazing MarshMello",
    author_email="srilalithansuresh@gmail.com",
    description="A Package That Converts Mixed Numbers To Improper Fractions And Vice Versa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TechGuru9000/mnif/tree/main",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
