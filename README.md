# Hospital Management System

**Autor:** Marcos Lorran B. Aguilar

## Sobre o Sistema
Este é um sistema simples de administração hospitalar desenvolvido como uma aplicação de linha de comando (CLI). O objetivo principal deste projeto é demonstrar a importância dos testes de software na manutenção e qualidade do código. O sistema permite o gerenciamento de pacientes, médicos e agendamento de consultas, garantindo a integridade dos dados e regras de negócio através de validações.

## Tecnologias Utilizadas
*   **Python 3**: Linguagem de programação principal.
*   **Pytest**: Framework para execução de testes unitários e de integração.
*   **Coverage.py**: Ferramenta para mensurar a cobertura de código dos testes.
*   **GitHub Actions**: Ferramenta de CI/CD para automação de testes em múltiplos sistemas operacionais (Linux, MacOS, Windows).
*   **Codecov**: Plataforma para hospedagem e análise de relatórios de cobertura de código.

## Como Executar os Testes Localmente

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd hospital-manager
    ```

2.  **Crie e ative um ambiente virtual (opcional, mas recomendado):**
    ```bash
    python -m venv venv
    # Linux/MacOS
    source venv/bin/activate
    # Windows
    venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute os testes:**
    ```bash
    pytest
    ```

5.  **Verifique a cobertura de testes:**
    ```bash
    coverage run -m pytest
    coverage report -m
    ```
    Para gerar um relatório HTML:
    ```bash
    coverage html
    # Abra o arquivo htmlcov/index.html no navegador
    ```
