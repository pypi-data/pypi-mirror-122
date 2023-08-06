import setuptools

import software_copyright_export_code

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setuptools.setup(
    name="software-copyright-export-code",
    version=software_copyright_export_code.__version__,
    author=software_copyright_export_code.__author__,
    author_email=software_copyright_export_code.__email__,
    description="Software copyright export code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panhaoyu/software-copyright-export-code",
    project_urls={
        "Bug Tracker": "https://github.com/panhaoyu/software-copyright-export-code/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=['demo*']),
    python_requires=">=3.8",
)
