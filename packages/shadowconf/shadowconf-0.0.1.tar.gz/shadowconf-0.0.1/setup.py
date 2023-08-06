from setuptools import find_packages, setup

setup(
    name="shadowconf",
    version="0.0.1",
    license="MIT",
    description="An elegant, dynamic, lightweight, reflective, productive, reproducible, and uninvasive Python yaml configuration framework. The shadow of your codebase.",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/ashleve/shadowconf",
    author="Łukasz Zalewski",
    author_email="lukasz.zalewski.ai@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8.0",
    include_package_data=True,
    install_requires=["python-dotenv>=0.20.0"],
    tests_require=["pytest"],
)
