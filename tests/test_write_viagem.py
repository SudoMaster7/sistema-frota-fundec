import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I').worksheet('DB_Viagens')

# Teste: adicionar uma viagem
print("Adicionando viagem de teste...")
test_viagem = [
    1,                          # ID
    "João Teste",               # Motorista
    "ABC-1234",                 # PlacaVeiculo
    "1000",                     # KmInicial
    "",                         # KmFinal
    "04/11/2025",              # DataSaida
    "12:00",                    # HoraSaida
    "",                         # DataChegada
    "",                         # HoraChegada
    "Teste Destino",            # Destinos
    "Em Rota",                  # Status
    "2",                        # Passageiros
    "Teste observações"         # Observacoes
]

sheet.append_row(test_viagem, value_input_option='RAW', table_range='A1:M1')
print("Viagem de teste adicionada!")

# Verificar
print("\nVerificando dados...")
headers = ['ID','Motorista','PlacaVeiculo','KmInicial','KmFinal','DataSaida','HoraSaida','DataChegada','HoraChegada','Destinos','Status','Passageiros','Observacoes']
records = sheet.get_all_records(expected_headers=headers)
print(f"Total viagens: {len(records)}")
if records:
    last = records[-1]
    print(f"\nÚltima viagem:")
    print(f"  ID: {last.get('ID')}")
    print(f"  Motorista: {last.get('Motorista')}")
    print(f"  Placa: {last.get('PlacaVeiculo')}")
    print(f"  Status: {last.get('Status')}")
