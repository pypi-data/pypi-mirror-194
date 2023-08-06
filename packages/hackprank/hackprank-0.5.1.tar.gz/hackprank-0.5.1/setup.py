from setuptools import setup, find_packages


VERSION = '0.5.1'
DESCRIPTION = 'A Python Package Full Of Fake Hacking Programs To Prank Your Friends'
LONG_DESCRIPTION = 'A Package That Lets You Easily Trick Your Friends And Prank Them With Fake Hacking Programs\n Version 0.3.3 Adds Matrix Fall Witch You Can Use With The New hackprank.matrix module\n Version 0.4.7 Adds New Matrix Fall hackprank.matrix '

# Setting up
setup(
    name="hackprank",
    version=VERSION,
    author="Aarav Goel",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['rich', 'flask', 'pyfiglet', 'flask', 'colorama'],
    keywords=['python', 'hack', 'prank', 'cool', 'pyhacks', 'pyhack', 'pranks', 'hackprank', 'hackpranks'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

    