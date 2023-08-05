from setuptools import setup

readme = ''
with open('README.md') as f:
    readme = f.read()


setup(
    name="discsocket",
    author="Tadeo Murillo",
    url="https://github.com/murillotadeo/discsocket",
    project_urls={
        "Issue tracker": "https://github.com/murillotadeo/discsocket/issues"
    },
    version="0.1.1",
    packages=['discsocket', 'discsocket.utils', 'discsocket.models'],
    license="MIT",
    description="Python framework for Discord interactions.",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=['aiohttp>=3.6.0,<3.8.0'],
    python_require=">=3.8.0",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)