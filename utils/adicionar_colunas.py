"""
Script para adicionar as colunas de Passageiros e Observacoes à planilha
Execute uma única vez para preparar a planilha
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

try:
    print("Conectando ao Google Sheets...")
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I')
    
    viagens_sheet = spreadsheet.worksheet("DB_Viagens")
    
    print("\n📋 Atualizando tabela DB_Viagens...")
    print("Adicionando colunas: Passageiros (L) e Observacoes (M)")
    
    # Adicionar header das novas colunas
    viagens_sheet.update_cell(1, 12, "Passageiros")
    viagens_sheet.update_cell(1, 13, "Observacoes")
    
    print("✅ Colunas adicionadas com sucesso!")
    print("\nNovas colunas:")
    print("  [12] Passageiros")
    print("  [13] Observacoes")
    
    # Preenchendo com valores padrão para registros antigos
    records = viagens_sheet.get_all_records()
    if len(records) > 0:
        print(f"\n📝 Preenchendo {len(records)} registros antigos com valores padrão...")
        for i, record in enumerate(records, 2):  # Começa da linha 2
            # Preencher com 0 passageiros e observações vazias
            viagens_sheet.update_cell(i, 12, "0")
            viagens_sheet.update_cell(i, 13, "")
        print("✅ Registros antigos atualizados!")
    
    print("\n" + "=" * 60)
    print("✅ PLANILHA ATUALIZADA COM SUCESSO!")
    print("=" * 60)
    print("\nAgora você pode usar o sistema com os novos campos:")
    print("  - Passageiros")
    print("  - Observacoes")
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
