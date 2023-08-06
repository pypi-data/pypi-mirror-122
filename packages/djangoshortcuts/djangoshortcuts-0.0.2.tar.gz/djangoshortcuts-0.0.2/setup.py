import setuptools

with open('README.md', 'r', encoding='utf-8') as fl:
    long_description = fl.read()

setuptools.setup(
    name="djangoshortcuts",
    version="0.0.2",
    author="Zhang",
    author_email="",
    description="Shortcuts to create files easily when using django",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/suifengpiaoyang/djangoshortcuts',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dj=djangoshortcuts.command:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5.2',
    license='MIT',
)
