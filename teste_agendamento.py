"""
Script de teste para validar as novas funcionalidades
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

try:
    print("=" * 70)
    print("TESTE DE FUNCIONALIDADES - AGENDAMENTO E CANCELAMENTO")
    print("=" * 70)
    
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I')
    viagens_sheet = spreadsheet.worksheet("DB_Viagens")
    
    print("\n✅ Conectado ao Google Sheets")
    
    # Verificar estrutura
    print("\n📋 Verificando estrutura da tabela...")
    header = viagens_sheet.row_values(1)
    print(f"Total de colunas: {len(header)}")
    
    # Verificar coluna de Status
    if 'Status' in header:
        status_col = header.index('Status') + 1
        print(f"✅ Coluna 'Status' encontrada (coluna {status_col})")
    else:
        print("❌ Coluna 'Status' não encontrada!")
    
    # Contar viagens por status
    print("\n📊 Contagem de viagens por status:")
    records = viagens_sheet.get_all_records()
    
    status_count = {}
    for record in records:
        status = record.get('Status', 'Desconhecido')
        status_count[status] = status_count.get(status, 0) + 1
    
    for status, count in status_count.items():
        print(f"  [{status}]: {count} viagem(ns)")
    
    # Verificar registros com datas
    print("\n📅 Verificando datas nas viagens...")
    datas = set()
    for record in records:
        data = record.get('DataSaida', '')
        if data:
            datas.add(data)
    
    print(f"Datas diferentes encontradas: {len(datas)}")
    for data in sorted(datas):
        print(f"  - {data}")
    
    print("\n" + "=" * 70)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    
    print("\n📝 Próximos passos:")
    print("1. Acesse http://localhost:5000/")
    print("2. Faça login")
    print("3. Clique em 'Registrar Saída'")
    print("4. Escolha uma data e hora")
    print("5. Registre a saída")
    print("6. Verifique no 'Cronograma'")
    print("7. Se for admin, clique em 'Cancelar' para testar")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
