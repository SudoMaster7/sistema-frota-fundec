import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I').worksheet('DB_Usuarios')

print("Verificando usuários sem telefone...")
usuarios = sheet.get_all_values()

# Cabeçalho deve ser: username, password_hash, role, telefone
header = usuarios[0]
print(f"Colunas atuais: {header}")

# Verificar se a coluna telefone existe
if len(header) < 4:
    print("Adicionando coluna 'telefone' ao cabeçalho...")
    sheet.update_cell(1, 4, 'telefone')
    header.append('telefone')

# Atualizar usuários que não têm telefone
usuarios_atualizados = 0
for idx, row in enumerate(usuarios[1:], 2):  # Começa da linha 2
    if len(row) < 4 or not row[3]:  # Se não tem telefone
        username = row[0] if len(row) > 0 else ''
        if username:
            print(f"Atualizando usuário '{username}' com telefone padrão...")
            sheet.update_cell(idx, 4, 'Não informado')
            usuarios_atualizados += 1

if usuarios_atualizados > 0:
    print(f"\n✅ {usuarios_atualizados} usuário(s) atualizado(s) com telefone padrão!")
else:
    print("\n✅ Todos os usuários já têm telefone cadastrado!")

print("\nVerificando resultado final...")
usuarios_final = sheet.get_all_records()
print(f"Total de usuários: {len(usuarios_final)}")
for u in usuarios_final:
    print(f"  - {u.get('username')}: {u.get('role')} | Tel: {u.get('telefone', 'N/A')}")
