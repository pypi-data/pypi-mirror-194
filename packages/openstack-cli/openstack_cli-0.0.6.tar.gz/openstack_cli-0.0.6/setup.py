import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def read_requirements():
    with open("requirements.txt") as req:
        content = req.read()
        requirements = content.split("\n")
    return requirements


setuptools.setup(
    name="openstack_cli",
    version="0.0.6",
    author="abdelrhman yasser",
    author_email="abdo.afage2@gmail.com",
    description="short package description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=read_requirements(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points="""
        [console_scripts]
        openstack=openstack_cli.cli:cli
    """,
    packages=setuptools.find_packages(),
    package_data={'openstack_cli': ['config/config.json']},
    python_requires=">=3.7",
    include_package_data=True,
)

