import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covidlag",
    version="0.0.4",
    author="yoshiyasu takefuji",
    author_email="takefuji@keio.jp",
    description="lag time and case fatality rate",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytakefuji/covidlag",
    project_urls={
        "Bug Tracker": "https://github.com/ytakefuji/covidlag",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['covidlag'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'covidlag = covidlag:main'
        ]
    },
)
