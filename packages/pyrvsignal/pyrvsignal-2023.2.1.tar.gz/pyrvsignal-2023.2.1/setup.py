import setuptools

import pyrvsignal

with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name="pyrvsignal",
    author="Ravikirana B",
    version=pyrvsignal.__version__,
    author_email="ravikiranb36@gmail.com",
    description="Signal for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ravikiranb36/pyrvsignal.github.io.git",
    license="MIT",
    packages=setuptools.find_packages(exclude=("tests", "venv")),
    include_package_data=True,
    package_data={},
    keywords='Signal PySignal pyrvsignal pyqtsignal ThreadSafe Signal',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    zip_safe=False,
)
