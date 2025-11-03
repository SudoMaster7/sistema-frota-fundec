"""
Script de diagnóstico para verificar a estrutura da planilha Google Sheets
Execute este script para entender melhor a estrutura dos dados
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuração
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]

try:
    # Conectar ao Google Sheets
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I')
    
    # Verificar tabela de viagens
    print("=" * 80)
    print("DIAGNÓSTICO DA PLANILHA GOOGLE SHEETS")
    print("=" * 80)
    
    # Tabela de Viagens
    print("\n📋 TABELA: DB_Viagens")
    print("-" * 80)
    viagens_sheet = spreadsheet.worksheet("DB_Viagens")
    viagens_header = viagens_sheet.row_values(1)
    print(f"Total de colunas: {len(viagens_header)}")
    print(f"Nomes das colunas:")
    for i, col in enumerate(viagens_header, 1):
        print(f"  [{i:2d}] {col}")
    
    # Verificar primeira linha de dados
    if viagens_sheet.row_count > 1:
        first_record = viagens_sheet.row_values(2)
        print(f"\nPrimeiro registro (linha 2):")
        print(f"Total de colunas preenchidas: {len(first_record)}")
        for i, val in enumerate(first_record[:15], 1):  # Mostrar até 15 colunas
            print(f"  [{i:2d}] {val[:50]}")  # Limitar a 50 caracteres
    
    # Tabela de Motoristas
    print("\n" + "=" * 80)
    print("📋 TABELA: DB_Motoristas")
    print("-" * 80)
    motoristas_sheet = spreadsheet.worksheet("DB_Motoristas")
    motoristas_header = motoristas_sheet.row_values(1)
    print(f"Total de colunas: {len(motoristas_header)}")
    print(f"Nomes das colunas:")
    for i, col in enumerate(motoristas_header, 1):
        print(f"  [{i:2d}] {col}")
    
    # Tabela de Veículos
    print("\n" + "=" * 80)
    print("📋 TABELA: DB_Veiculos")
    print("-" * 80)
    veiculos_sheet = spreadsheet.worksheet("DB_Veiculos")
    veiculos_header = veiculos_sheet.row_values(1)
    print(f"Total de colunas: {len(veiculos_header)}")
    print(f"Nomes das colunas:")
    for i, col in enumerate(veiculos_header, 1):
        print(f"  [{i:2d}] {col}")
    
    # Tabela de Usuários
    print("\n" + "=" * 80)
    print("📋 TABELA: DB_Usuarios")
    print("-" * 80)
    usuarios_sheet = spreadsheet.worksheet("DB_Usuarios")
    usuarios_header = usuarios_sheet.row_values(1)
    print(f"Total de colunas: {len(usuarios_header)}")
    print(f"Nomes das colunas:")
    for i, col in enumerate(usuarios_header, 1):
        print(f"  [{i:2d}] {col}")
    
    print("\n" + "=" * 80)
    print("✅ Diagnóstico completado com sucesso!")
    print("=" * 80)
    
except Exception as e:
    print(f"❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
