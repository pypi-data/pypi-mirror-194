import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='ssd-scheduler',  # should match the package folder
    packages=['ssd-scheduler'],  # should match the package folder
    version='v1.2',  # important for updates
    license='MIT',  # should match your chosen license
    description='Testing installation of Package',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Test user',
    author_email='test@gmail.com',
    url='https://murathanov-stepan.ru/gitea/sa/ssd-scheduler.git',
    project_urls={  # Optional
        "Bug Tracker": "https://murathanov-stepan.ru/gitea/sa/ssd-scheduler.git"
    },
    install_requires=['requests'],  # list all packages that your package uses
    keywords=["pypi", "ssd-scheduler", "test"],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],

    download_url="https://murathanov-stepan.ru/gitea/sa/ssd-scheduler/archive/v1.2.tar.gz",
)
