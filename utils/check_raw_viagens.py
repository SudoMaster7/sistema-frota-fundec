import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I').worksheet('DB_Viagens')

# Ver os dados brutos
print('Linha 1 (cabeçalhos):')
header = sheet.row_values(1)
for idx, h in enumerate(header[:20], 1):
    print(f'  Col {idx}: "{h}"')

print('\nÚltimas 3 linhas de dados:')
all_values = sheet.get_all_values()
for row_idx, row in enumerate(all_values[-3:], len(all_values)-2):
    print(f'\nLinha {row_idx}:')
    for col_idx, val in enumerate(row[:15], 1):
        if val:
            print(f'  Col {col_idx}: "{val}"')
