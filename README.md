# Sistema de Controle de Frota - FUNDEC

Sistema web desenvolvido em Python com Flask para o gerenciamento e controle de viagens da frota de veículos da FUNDEC.

## ✨ Funcionalidades

- **Controle de Viagens:** Registro de saída e chegada de veículos.
- **Gestão de Dados:** Adição de novos motoristas, veículos e usuários do sistema.
- **Sistema de Login:** Autenticação segura com diferenciação de permissões (Admin vs. Usuário/Motorista).
- **Relatórios Diários:** Geração de relatórios de quilometragem por veículo e por motorista, com consulta por data.
- **Interface Moderna:** Estilo baseado em Bootstrap 5 com seletor de tema (modo claro/escuro).
- **Persistência de Dados:** Integração direta com planilhas do Google Sheets para armazenamento de dados.

## 🚀 Tecnologias Utilizadas

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript
- **Banco de Dados:** Google Sheets API
- **Autenticação:** Flask-Login, Flask-Bcrypt

## ⚙️ Como Executar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
    cd SEU-REPOSITORIO
        ```

## 📦 Dependências

Veja `requirements.txt` (Flask, gspread, oauth2client, Flask-Login, Flask-Bcrypt, pytz).

## 🔐 Credenciais do Google (alternativa com variável de ambiente)

No PowerShell (Windows), você pode usar o conteúdo do `credentials.json` diretamente:

```powershell
$env:GOOGLE_CREDENTIALS_JSON = Get-Content -Raw -Path .\credentials.json
```

## 🧱 Estrutura de dados (Google Sheets)

- DB_Usuarios: [username, password_hash, role, telefone]
- DB_Veiculos: [Modelo, Placa, Ano, Status]
- DB_Agendamentos (A:O): ID, DataAgendamento, Motorista, PlacaVeiculo, DataSolicitada, HoraInicio, HoraFim, Destinos, Passageiros, Observacoes, Status, MotivoCancelamento, DataCancelamento, Observacoes_Admin, UltimaAtualizacao
    - Observacoes_Admin armazena: `Novo agendamento (Agendado por: <username>)`
- DB_Viagens (A:M): ID, Motorista, PlacaVeiculo, KmInicial, KmFinal, DataSaida, HoraSaida, DataChegada, HoraChegada, Destinos, Status, Passageiros, Observacoes
    - Inserções usam `table_range='A1:M1'` para manter alinhamento

## 🧭 Como usar (visão geral)

- Agendamentos
    - Filtros: Status, Placa, Motorista, Data (de/até) e “Somente futuros/ativos”
    - Ordenação: datas mais próximas primeiro; dentro do dia, mais novos no topo
    - Ações rápidas (admin): Confirmar; Registrar Saída (Confirmado); Registrar Chegada (Em Uso)
    - Card mostra “Agendado por” (quem criou) e “Contato” (telefone)
- Cronograma
    - Todos os usuários visualizam veículos “Em Rota”, com motorista, agendado por, contato, destinos e horários
- Registrar Saída (admin)
    - Seleciona agendamento confirmado/agendado, informa KM inicial
    - Data/hora são do momento atual (America/Sao_Paulo); valida antecipação
- Registrar Chegada (admin)
    - Seleciona veículo “Em Uso” e informa KM final; viagem é finalizada e veículo liberado

## 🛠️ Troubleshooting

- Cronograma com erro de cabeçalho: código usa fallback de headers esperados
- Viagens não aparecem: verifique Status “Em Rota” e colunas alinhadas em `DB_Viagens`
- Dados desalinhados: limpe linhas corrompidas e mantenha `table_range='A1:M1'`

## 📄 Licença

Uso interno. Ajuste conforme a política da organização.

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install Flask gspread oauth2client Flask-Login Flask-Bcrypt
    ```

4.  **Configure as credenciais do Google:**
    - Siga o tutorial da API do Google para gerar um arquivo `credentials.json`.
    - Coloque este arquivo na raiz do projeto.
    - Compartilhe sua planilha do Google com o `client_email` encontrado no arquivo de credenciais.

5.  **Execute a aplicação:**
    ```bash
    flask run
    ```
