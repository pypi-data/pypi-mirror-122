import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bee-movie',
    version='4.2.0',
    description='A package to easy insert the Bee Movie script into any Python project.',
    url='https://github.com/noahgarrett/BeePython',
    author='Noah Garrett',
    author_email='noah.garrett@jerboatechnologies.com',
    license='MIT',
    packages=setuptools.find_packages(where="src"),
    install_requires=[],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    package_dir={"": "src"},
)