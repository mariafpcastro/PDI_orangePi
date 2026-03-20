# Projeto de Controle de Hardware Embarcado

Este projeto consiste em uma biblioteca modular desenvolvida em Python para sistemas Linux embarcados (como Raspberry Pi, BeagleBone e similares). A estrutura foi projetada para separar a lógica de negócio da abstração de hardware, permitindo o desenvolvimento e testes tanto em ambiente local quanto no alvo (target).

## Estrutura do Projeto

* **QAT/**: Pacote principal contendo a lógica da biblioteca e abstrações de hardware.
* **examples/**: Demonstrações de implementação da biblioteca.
* **tests/**: Testes unitários e de integração.
* **main.py**: Script de entrada para testes rápidos e validação em tempo de desenvolvimento.
* **setup.py**: Script de configuração para instalação do pacote via pip.
* **requirements.txt**: Lista de dependências do projeto.

## Pré-requisitos

* Python 3.7 ou superior.

## Instalação e Configuração

### 1. Criação do Ambiente Virtual

É altamente recomendável o uso de um ambiente virtual para isolar as dependências do projeto e evitar conflitos com as bibliotecas do sistema operacional.

```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual (Linux/macOS)
source venv/bin/activate

# No Windows (se aplicável)
# .\venv\Scripts\activate
```

### 2. Instalação das Dependências

Com o ambiente virtual ativo, instale as dependências listadas no arquivo requirements.txt:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Instalação em Modo de Desenvolvimento

Para que a biblioteca seja reconhecida pelo Python em qualquer local do sistema, mas permita que alterações no código fonte sejam refletidas instantaneamente, instale-a em modo editável:

```bash
pip install -e .
```

## Uso da Biblioteca

A biblioteca pode ser importada em qualquer script Python dentro do ambiente virtual. Abaixo, um exemplo básico de utilização:

```python
from my_library import SensorController

# Instancia o controlador
controller = SensorController(pin=18)

# Executa a lógica de alerta
controller.run_alert()
```

Para executar o script de teste incluído na raiz do projeto:

```bash
python main.py
```

## Fluxo de Desenvolvimento

### Modificando a Biblioteca

Graças à instalação com a flag -e, as modificações realizadas nos arquivos dentro da pasta QAT/ não exigem uma nova instalação. Basta salvar os arquivos e reiniciar a execução do seu script de teste ou aplicação.

### Gerenciamento de Dependências

Caso novas bibliotecas externas sejam necessárias:

1. Adicione a dependência ao arquivo requirements.txt.
2. Atualize o seu ambiente local com pip install -r requirements.txt.
3. O arquivo setup.py está configurado para ler automaticamente estas alterações no momento de uma nova instalação.

## Testes

Os testes devem ser colocados na pasta tests/ e podem ser executados utilizando o pytest (caso instalado):

```bash
pip install pytest
pytest
```

---

**Nota:** Certifique-se de não versionar arquivos temporários ou o ambiente virtual. O arquivo .gitignore já está configurado para ignorar estas pastas.
