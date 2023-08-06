from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as readme_file:
    readme = readme_file.read()

setup(
    name="getindianname",
    version="1.0.7",
    author="Devesh Singh",
    url="https://github.com/TechUX/getindianname",
    description="Generate names based on India. Generate more than 70K unique name within 5 seconds. Names Automaticaly added and updated. About 10+ names were added daily.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["getindianname"],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'name = getindianname.main:main',
            'indianname = getindianname.main:main',
        ],
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ]
)