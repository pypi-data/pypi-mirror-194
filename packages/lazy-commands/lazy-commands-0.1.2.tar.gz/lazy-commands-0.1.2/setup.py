from setuptools import setup, find_packages

setup(
    name='lazy-commands',
    version='0.1.2',
    scripts=['gptshell/lazycmd.py'],
    author='minhalvp (Minhal Valiya Peedikakkal)',
    description='A simple command line interface which converts a description of a command into the command itself and vice versa.',
    install_requires=['typer', 'langchain'],
    packages=find_packages(),
    keywords=['python','langchain','gpt','openai','cli'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)