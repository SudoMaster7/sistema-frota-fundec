import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define o escopo de acesso da API
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

# Aponta para o arquivo de credenciais JSON
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

# Autoriza o cliente
client = gspread.authorize(creds)
#1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I
# Abre a planilha pelo NOME EXATO que você deu a ela no Google Sheets
try:
    spreadsheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I')
    print("Conexão com a planilha bem-sucedida!")

    # Pega a primeira aba (worksheet) da planilha
    worksheet = spreadsheet.worksheet("DB_Motoristas") # Use o nome exato da sua aba
    
    # Exemplo: Pega todos os registros da aba de motoristas
    motoristas = worksheet.get_all_records()
    
    print("\nMotoristas encontrados na planilha:")
    for motorista in motoristas:
        print(f"- {motorista['Nome']} (Matrícula: {motorista['Matricula']})")

except gspread.exceptions.SpreadsheetNotFound:
    print("\nERRO: Planilha não encontrada!")
    print("Verifique se o nome da planilha está correto no código e se você a compartilhou com o e-mail da conta de serviço.")
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")