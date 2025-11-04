#!/usr/bin/env python3
"""
Script para configurar a planilha de agendamentos no Google Sheets
Adiciona uma nova aba "DB_Agendamentos" com estrutura apropriada
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

def setup_agendamentos():
    """Cria a planilha de agendamentos com as colunas necessárias."""
    
    try:
        # Autenticar com Google Sheets
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive.file'
        ]
        
        # Tenta usar variável de ambiente primeiro (para deploy)
        creds_json_str = os.environ.get('GOOGLE_CREDENTIALS_JSON')
        if creds_json_str:
            creds_dict = json.loads(creds_json_str)
            creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        else:
            # Fallback para arquivo local
            creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I')
        
        # Tentar obter ou criar planilha de agendamentos
        try:
            agendamentos_sheet = spreadsheet.worksheet("DB_Agendamentos")
            print("✅ Planilha DB_Agendamentos já existe!")
        except:
            print("📝 Criando planilha DB_Agendamentos...")
            agendamentos_sheet = spreadsheet.add_worksheet(title="DB_Agendamentos", rows=1000, cols=15)
            
            # Adicionar headers
            headers = [
                "ID",                    # A
                "DataAgendamento",       # B (Data do agendamento - quando foi criado)
                "Motorista",             # C
                "PlacaVeiculo",          # D
                "DataSolicitada",        # E (Data desejada para usar o veículo)
                "HoraInicio",            # F (Hora de início - quando quer sair)
                "HoraFim",               # G (Hora de término - quando quer voltar)
                "Destinos",              # H
                "Passageiros",           # I
                "Observacoes",           # J
                "Status",                # K (Agendado, Confirmado, Em Uso, Finalizado, Cancelado)
                "MotivoCancelamento",    # L
                "DataCancelamento",      # M
                "Observacoes_Admin",     # N
                "UltimaAtualizacao"      # O
            ]
            
            agendamentos_sheet.insert_row(headers, 1)
            print("✅ Headers adicionados com sucesso!")
            
            # Adicionar dados de exemplo
            exemplo = [
                "1",                             # ID
                "04/11/2025",                    # DataAgendamento
                "João Silva",                    # Motorista
                "ABC-1234",                      # PlacaVeiculo
                "10/11/2025",                    # DataSolicitada
                "08:00",                         # HoraInicio
                "17:00",                         # HoraFim
                "Centro da Cidade",              # Destinos
                "5",                             # Passageiros
                "Viagem de negócios",            # Observacoes
                "Agendado",                      # Status
                "",                              # MotivoCancelamento
                "",                              # DataCancelamento
                "Aguardando confirmação",        # Observacoes_Admin
                "04/11/2025 10:00"               # UltimaAtualizacao
            ]
            agendamentos_sheet.insert_row(exemplo, 2)
            print("✅ Exemplo de agendamento adicionado!")
        
        print("\n" + "="*60)
        print("✅ SETUP CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print("\nPlanilha de Agendamentos:")
        print("- ID: Identificador único")
        print("- DataAgendamento: Quando foi solicitado")
        print("- Motorista: Nome do motorista")
        print("- PlacaVeiculo: Placa do veículo")
        print("- DataSolicitada: Que dia quer usar")
        print("- HoraInicio: Que hora quer começar")
        print("- HoraFim: Que hora quer terminar")
        print("- Destinos: Onde vai")
        print("- Passageiros: Quantas pessoas")
        print("- Observacoes: Observações do motorista")
        print("- Status: Agendado/Confirmado/Em Uso/Finalizado/Cancelado")
        print("- MotivoCancelamento: Se foi cancelado, por qual motivo")
        print("- DataCancelamento: Quando foi cancelado")
        print("- Observacoes_Admin: Notas do administrador")
        print("- UltimaAtualizacao: Última vez que foi alterado")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("🚀 Iniciando setup de agendamentos...\n")
    setup_agendamentos()
