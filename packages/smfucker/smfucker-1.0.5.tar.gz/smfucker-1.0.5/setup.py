import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smfucker",
    version="1.0.5",
    author="The_Itach1",
    author_email="2507709326@qq.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/The-Itach1//smfucker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
    ],
    python_requires='>=3',
    entry_points = {
        'console_scripts': [
            'smfucker = smfucker.smfucker:exe_main',
        ],
    }
)