from setuptools import setup, find_packages

with open("README.md") as file:
    readme = file.read()

with open("requirements.txt") as file:
    requirements = [req for req in file.read().split("\n") if req and not req.startswith("#")]


setup(
    name="pycosnippets",
    version="0.1.0",
    description="Python Code Snippets",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="rhdzmota",
    author_email='contact@rhdzmota.com',
    url="https://github.com/rhdzmota/pycosnippets",
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    package_dir={
        "": "src"
    },
    package_data={
        "": [
            "templates/default.ipynb"
        ]
    },
    packages=find_packages(where='src'),
    include_package_data=True,
    scripts=[
        "bin/pycosnippets"
    ],
    install_requires=requirements,
    python_requires='>=3.7, <3.8',
    license="MIT",
)
