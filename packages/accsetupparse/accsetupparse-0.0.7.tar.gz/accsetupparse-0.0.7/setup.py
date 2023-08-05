from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: GPLv3 License',
  'Programming Language :: Python :: 3'
]

setup(
    name="accsetupparse",
    version="0.0.7",
    description="Library for converting and storing ACC json setups into Python class",
    url="https://github.com/jura43/acc-setup-parse",
    long_description=open("README.md").read() + '\n\n' + open('CHANGELOG.md').read(),
    long_description_content_type="text/markdown",
    author="Jurica Slovinac",
    packages=find_packages(exclude=["main.py", ".gitignore", ".git", "test.json", "Untitled-1.txt"]),
    keywords='parser',
    license="GPLv3",
    project_urls = {
      'Home': 'https://github.com/jura43/acc-setup-parse',
      'Changelog': 'https://github.com/jura43/acc-setup-parse/blob/master/README.md'
}
)