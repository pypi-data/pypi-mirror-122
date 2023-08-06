from setuptools import setup, find_packages

setup(
    install_requires=["openseespy","numpy","matplotlib"],
    name='utpl-modelos-columnas',
    version='4.0',
    description='Modelos de Columnas- Tesis de Grado',
    author='Ronald Valencia',
    author_email='ravalencia2@utpl.edu.ec',
    url='https://github.com/ravalenciaochoa/utpl',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ]
)
