from setuptools import setup

setup(
    name="TP2_Package_Robot_Jomain",
    author="Jomain Benoît",
    version="0.1",
    description="Génération d'une grille avec des méthodes qui permettent de déplacer un robot sur cette grille",
    packages=["Package_Robot"],
    install_requires=[
        "numpy",
        "pytest",
    ],
)

