from distutils.core import setup

global README

with open('README.md', 'r', encoding="utf-8") as f:
  README = f.read()

setup(
    name='linelib',
    version='2.2.2',
    packages=['linelib', 'linelib.notify', 'linelib.ext', 'linelib.connect', 'linelib.model'],
    license='MIT',
    description="The solution to simplicity.",
    long_description=README,
    long_description_content_type="text/markdown",
    author='AWeirdScratcher',
    author_email = "aweirdscrather@gmail.com",
    install_requires=[
        'httpx', 'urllib3', 'flask', 'flask-cors', 'termcolor', 'tqdm'
    ],
    keywords = ['line', 'bot', 'line bot', 'sdk', 'line notify', 'commands'],
    url="https://github.com/AWeirdScratcher/linelib",
    classifiers=[
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10'
  ]
)