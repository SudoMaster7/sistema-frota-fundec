import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I').worksheet('DB_Usuarios')

print("Verificando estrutura da planilha DB_Usuarios...")
header = sheet.row_values(1)
print(f"Cabeçalhos atuais: {header}")

# Adicionar cabeçalho 'telefone' se não existir
if len(header) < 4 or header[3] != 'telefone':
    print("Adicionando cabeçalho 'telefone' na coluna D...")
    sheet.update_cell(1, 4, 'telefone')
    print("Cabeçalho adicionado!")

# Atualizar usuários existentes com telefone padrão se necessário
all_rows = sheet.get_all_values()
print(f"\nTotal de linhas: {len(all_rows)}")

for idx, row in enumerate(all_rows[1:], 2):  # Pula o cabeçalho
    if len(row) < 4 or not row[3]:  # Se não tem telefone
        username = row[0] if len(row) > 0 else 'N/A'
        print(f"  Linha {idx} (usuário: {username}) - adicionando telefone padrão...")
        sheet.update_cell(idx, 4, '00000000000')

print("\n✅ Atualização concluída! Todos os usuários agora têm um campo de telefone.")
print("   Você pode editar manualmente na planilha ou pelo sistema.")
