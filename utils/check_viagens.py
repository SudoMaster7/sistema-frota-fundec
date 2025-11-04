import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I').worksheet('DB_Viagens')

headers = ['ID','Motorista','PlacaVeiculo','KmInicial','KmFinal','DataSaida','HoraSaida','DataChegada','HoraChegada','Destinos','Status','Passageiros','Observacoes']

try:
    records = sheet.get_all_records(expected_headers=headers)
    print(f'Total viagens: {len(records)}')
    print('\nÚltimas 5 viagens:')
    for r in records[-5:]:
        print(f'ID:{r.get("ID")} Status:"{r.get("Status")}" Placa:{r.get("PlacaVeiculo")} Data:{r.get("DataSaida")}')
    
    print('\nViagens "Em Rota":')
    em_rota = [v for v in records if v.get('Status') == 'Em Rota']
    print(f'Total Em Rota: {len(em_rota)}')
    for v in em_rota:
        print(f'  - ID:{v.get("ID")} Placa:{v.get("PlacaVeiculo")} Motorista:{v.get("Motorista")}')
except Exception as e:
    print(f'Erro: {e}')
