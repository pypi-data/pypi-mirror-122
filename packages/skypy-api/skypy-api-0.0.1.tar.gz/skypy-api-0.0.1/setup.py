import setuptools


setuptools.setup(
    name="skypy-api",
    url="https://github.com/FuchsCrafter/skypy",
    version="0.0.1",
    author="FuchsCrafter",
    license="MIT",
    description="Framework to connect to the Hypixel Skyblock API",
    long_description="Framework to connect to the Hypixel Skyblock API",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
    install_requires=["requests"]
)
