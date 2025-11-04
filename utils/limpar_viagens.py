import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I').worksheet('DB_Viagens')

# Deletar linhas com dados nas colunas erradas (linhas 2 em diante)
print("Limpando dados corrompidos...")
all_values = sheet.get_all_values()
total_rows = len(all_values)

if total_rows > 1:
    # Manter apenas o cabeçalho (linha 1)
    sheet.resize(rows=1)
    print(f"Deletadas {total_rows-1} linhas corrompidas")
else:
    print("Nenhuma linha para deletar")

print("Planilha DB_Viagens limpa e pronta!")
