from setuptools import setup

with open("README.md", "rb") as f:
    long_descr = f.read().decode()

with open("requirements.txt", "rb") as f:
    requirements = f.read().decode().splitlines()

setup(
    name="betting-game-backend",
    packages=["app"],
    version="0.1.0",
    description="Backend for soccer betting game.",
    long_description=long_descr,
    author="Tobias Happ",
    author_email="tobias.happ@gmx.de",
    url="https://github.com/Gerschtli/betting-game-backend",
    license="MIT",
    install_requires=requirements,
)
