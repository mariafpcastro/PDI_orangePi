from setuptools import setup, find_packages
import os

# Função para ler o requirements.txt
def parse_requirements(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="QAT",
    version="0.1.0",
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    author="Seu Nome",
    description="Biblioteca embarcada com dependências dinâmicas",
    python_requires=">=3.7",
)
