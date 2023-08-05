from setuptools import setup, find_packages

setup(
    name = 'sleepyask',
    version = '0.0.1',
    author = 'hwelsters',
    author_email = 'redacted@redacted.redacted',
    description = 'Tool for asking gathering responses from ChatGPT without user attention',
    url = 'https://github.com/hwelsters/sleepyask',
    license = 'BSD 3-clause',
    project_urls = {
        'Bug Tracker': 'https://github.com/hwelsters/sleepyask/issues',
        'Repository': 'https://github.com/hwelsters/sleepyask'
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ],
    python_requires = '>3.6',
    install_requires = [
        'schedule==1.1.0',
        'revChatGPT==2.3.6'
    ],
    packages = find_packages(),
    include_package_data=True
)