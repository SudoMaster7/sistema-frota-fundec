import gspread
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz
import os
import json

# --- CONFIGURAÇÃO INICIAL ---
app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

# --- CONFIGURAÇÃO DO FLASK-LOGIN ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redireciona para a página de login se não estiver logado
login_manager.login_message = "Por favor, faça o login para acessar esta página."
login_manager.login_message_category = "info"


# --- CONEXÃO COM GOOGLE SHEETS ---
try:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive.file']

    # Tenta primeira: variável de ambiente (PRODUÇÃO)
    creds_json_str = os.environ.get('GOOGLE_CREDENTIALS_JSON')
    
    if creds_json_str:
        # Produção: usar variável de ambiente
        print("📌 Usando credenciais da variável de ambiente GOOGLE_CREDENTIALS_JSON")
        creds_dict = json.loads(creds_json_str)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    else:
        # Desenvolvimento: tentar arquivo local
        try:
            print("📌 Buscando arquivo credentials.json local...")
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                'credentials.json',
                scope
            )
            print("✅ Usando arquivo credentials.json local")
        except FileNotFoundError:
            raise ValueError(
                "\n❌ ERRO: Não foi possível conectar ao Google Sheets.\n"
                "   Configure uma das opções:\n"
                "   1. Adicione 'credentials.json' na pasta raiz\n"
                "   2. Configure a variável de ambiente GOOGLE_CREDENTIALS_JSON\n"
                "   Veja 'CONFIGURAR_CREDENCIAIS.md' para mais detalhes."
            )
    
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key('1ZjTYIRF_n91JSCI1OytRYaRFiGkZX2JgoqB0eRIwu8I')
    
    # Carrega todas as planilhas
    viagens_sheet = spreadsheet.worksheet("DB_Viagens")
    motoristas_sheet = spreadsheet.worksheet("DB_Motoristas")
    veiculos_sheet = spreadsheet.worksheet("DB_Veiculos")
    usuarios_sheet = spreadsheet.worksheet("DB_Usuarios")
    agendamentos_sheet = spreadsheet.worksheet("DB_Agendamentos")
    
    print("✅ Conexão com Google Sheets estabelecida com sucesso!")
except Exception as e:
    print(f"\n❌ ERRO CRÍTICO ao conectar com Google Sheets:\n   {e}")
    print("\n💡 Solução: Consulte 'CONFIGURAR_CREDENCIAIS.md' para instruções")
    # Em um ambiente de produção, você pode querer lidar com isso de forma mais elegante
    # Por enquanto, vamos parar a aplicação se a conexão falhar.
    exit()

# --- MODELO DE USUÁRIO ---
class User(UserMixin):
    def __init__(self, id, password_hash, role, telefone=None):
        self.id = id
        self.password_hash = password_hash
        self.role = role
        self.telefone = telefone

    @staticmethod
    def get(user_id):
        try:
            user_data = usuarios_sheet.find(user_id)
            user_row = usuarios_sheet.row_values(user_data.row)
            # Suporta usuários antigos sem telefone (coluna 4)
            telefone = user_row[3] if len(user_row) > 3 else None
            return User(id=user_row[0], password_hash=user_row[1], role=user_row[2], telefone=telefone)
        except Exception as e:
            return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash("Acesso restrito a administradores.", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function
# --- ROTAS DE AUTENTICAÇÃO ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get(username)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# --- FUNÇÕES AUXILIARES ---
def get_all_records(sheet):
    """Retorna todos os registros da planilha, ignorando colunas vazias extras."""
    try:
        return sheet.get_all_records()
    except Exception as e:
        # Se houver erro de cabeçalhos duplicados, tentar com cabeçalhos esperados
        if "duplicates" in str(e):
            # Para DB_Viagens, especificar os cabeçalhos corretos
            if "Viagens" in sheet.title:
                expected = ['ID', 'Motorista', 'PlacaVeiculo', 'KmInicial', 'KmFinal', 
                           'DataSaida', 'HoraSaida', 'DataChegada', 'HoraChegada', 
                           'Destinos', 'Status', 'Passageiros', 'Observacoes']
                return sheet.get_all_records(expected_headers=expected)
        raise

# --- ROTAS PRINCIPAIS ---

@app.route('/')
@login_required
def index():
    """Dashboard principal com resumo das atividades."""
    # Estatísticas gerais
    viagens_em_rota = [v for v in get_all_records(viagens_sheet) if v['Status'] == 'Em Rota']
    viagens_finalizadas_hoje = []
    
    hoje = datetime.now().strftime('%d/%m/%Y')
    for v in get_all_records(viagens_sheet):
        if v['Status'] == 'Finalizada' and v['DataSaida'] == hoje:
            viagens_finalizadas_hoje.append(v)
    
    total_veiculos = len(veiculos_sheet.get_all_records())
    veiculos_disponiveis = len([v for v in veiculos_sheet.get_all_records() if v['Status'] == 'Disponível'])
    veiculos_em_uso = len([v for v in veiculos_sheet.get_all_records() if v['Status'] == 'Em Uso'])
    
    # Para motoristas, mostrar apenas seu próprio painel
    motoristas = []
    if current_user.role == 'admin':
        motoristas = motoristas_sheet.get_all_records()
    
    veiculos_disponiveis_list = [v for v in veiculos_sheet.get_all_records() if v['Status'] == 'Disponível']
    
    # Calcular distância total do dia
    distancia_total_hoje = 0
    for v in viagens_finalizadas_hoje:
        try:
            km_inicial = int(v.get('KmInicial', 0))
            km_final = int(v.get('KmFinal', 0))
            if km_final > km_inicial:
                distancia_total_hoje += (km_final - km_inicial)
        except:
            pass
    
    contexto = {
        'motoristas': motoristas,
        'veiculos': veiculos_disponiveis_list,
        'current_user': current_user,
        # Estatísticas
        'viagens_em_rota': len(viagens_em_rota),
        'viagens_hoje': len(viagens_finalizadas_hoje),
        'total_veiculos': total_veiculos,
        'veiculos_disponiveis': veiculos_disponiveis,
        'veiculos_em_uso': veiculos_em_uso,
        'distancia_hoje': distancia_total_hoje
    }
    
    return render_template('index.html', **contexto)


@app.route('/registrar-saida', methods=['GET', 'POST'])
@admin_required
def registrar_saida():
    """Página e processamento para Registrar Saída (apenas admin)."""
    try:
        # Se for GET, renderiza o formulário em página dedicada
        if request.method == 'GET':
            # Listar agendamentos elegíveis (Confirmado/Agendado) para hoje ou datas futuras
            ag_list = agendamentos_sheet.get_all_records()
            agendamentos_disponiveis = [a for a in ag_list if a.get('Status') in ['Confirmado', 'Agendado']]
            # Pré-selecionar via querystring (atalho vindo da lista de agendamentos)
            agendamento_id_qs = request.args.get('agendamento_id')
            agendamento_selecionado = None
            if agendamento_id_qs:
                for a in agendamentos_disponiveis:
                    if str(a.get('ID')) == str(agendamento_id_qs):
                        agendamento_selecionado = a
                        break
            return render_template('registrar_saida.html', agendamentos=agendamentos_disponiveis, agendamento_selecionado=agendamento_selecionado)

        # POST: registrar saída com base em um agendamento selecionado
        agendamento_id = request.form.get('agendamento_id')
        if not agendamento_id:
            flash('Selecione um agendamento para registrar a saída.', 'danger')
            return redirect(url_for('registrar_saida'))

        # Encontrar o agendamento e sua linha na planilha
        ag_list = agendamentos_sheet.get_all_records()
        agendamento = None
        agendamento_row = None
        for idx, a in enumerate(ag_list, 2):
            if str(a.get('ID')) == str(agendamento_id):
                agendamento = a
                agendamento_row = idx
                break
        if not agendamento:
            flash('Agendamento não encontrado.', 'danger')
            return redirect(url_for('registrar_saida'))
        if agendamento.get('Status') not in ['Confirmado', 'Agendado']:
            flash('Este agendamento não está elegível para registro de saída.', 'warning')
            return redirect(url_for('registrar_saida'))

        # Dados vindos do agendamento
        motorista = agendamento.get('Motorista')
        placa = agendamento.get('PlacaVeiculo')
        destinos = agendamento.get('Destinos', '')
        passageiros = agendamento.get('Passageiros', '0')
        obs_agendamento = agendamento.get('Observacoes', '')

        # Campo obrigatório no formulário
        km_inicial = request.form.get('km_inicial')
        observacoes_extra = request.form.get('observacoes', '')
        antecipar = request.form.get('antecipar', 'nao')
        
        if not km_inicial:
            flash('Informe o KM inicial.', 'danger')
            return redirect(url_for('registrar_saida'))

        # Definir data/hora atuais em São Paulo
        fuso_horario_sp = pytz.timezone("America/Sao_Paulo")
        agora = datetime.now(fuso_horario_sp)
        data_saida = agora.strftime('%d/%m/%Y')
        hora_saida = agora.strftime('%H:%M')
        
        # Validar se a saída está sendo feita dentro do horário agendado
        data_agendada = agendamento.get('DataSolicitada', '')
        hora_inicio_agendada = agendamento.get('HoraInicio', '')
        hora_fim_agendada = agendamento.get('HoraFim', '')
        
        # Verificar se é o mesmo dia
        if data_saida == data_agendada:
            # Comparar horários
            hora_atual_min = int(agora.strftime('%H')) * 60 + int(agora.strftime('%M'))
            try:
                h_ini, m_ini = hora_inicio_agendada.split(':')
                hora_inicio_min = int(h_ini) * 60 + int(m_ini)
                
                if hora_atual_min < hora_inicio_min:
                    # Saída antecipada - precisa confirmação
                    diferenca_min = hora_inicio_min - hora_atual_min
                    horas_diff = diferenca_min // 60
                    minutos_diff = diferenca_min % 60
                    
                    if antecipar != 'sim':
                        msg = f'⏰ O agendamento está marcado para começar às {hora_inicio_agendada} '
                        msg += f'(daqui a {horas_diff}h{minutos_diff}min). '
                        msg += 'Deseja antecipar a saída?'
                        flash(msg, 'warning')
                        # Renderizar novamente com opção de confirmação
                        ag_list = agendamentos_sheet.get_all_records()
                        agendamentos_disponiveis = [a for a in ag_list if a.get('Status') in ['Confirmado', 'Agendado']]
                        return render_template('registrar_saida.html', 
                                             agendamentos=agendamentos_disponiveis,
                                             agendamento_selecionado=agendamento,
                                             km_inicial=km_inicial,
                                             observacoes=observacoes_extra,
                                             aviso_antecipacao=msg)
            except:
                pass  # Se houver erro ao parsear horário, continuar normalmente

        # Nova viagem com estrutura compatível com a planilha
        nova_viagem = [
            len(get_all_records(viagens_sheet)) + 2,  # ID
            motorista,                                  # Motorista
            placa,                                      # PlacaVeiculo
            km_inicial,                                 # KmInicial
            "",                                         # KmFinal (vazio, será preenchido na chegada)
            data_saida,                                 # DataSaida
            hora_saida,                                 # HoraSaida
            "",                                         # DataChegada (vazio, será preenchido na chegada)
            "",                                         # HoraChegada (vazio, será preenchido na chegada)
            destinos,                                   # Destinos
            "Em Rota",                                  # Status
            passageiros,                                # Passageiros
            f"[Agendamento ID: {agendamento_id}] " + (observacoes_extra or obs_agendamento or '')  # Observacoes
        ]
        # Escrever na próxima linha disponível nas colunas A:M (colunas 1-13)
        next_row = len(viagens_sheet.get_all_values()) + 1
        viagens_sheet.append_row(nova_viagem, value_input_option='RAW', table_range='A1:M1')

        # Atualizar status do veículo
        try:
            cell = veiculos_sheet.find(placa)
            veiculos_sheet.update_cell(cell.row, 4, "Em Uso")
        except Exception as e:
            flash(f'AVISO: Placa {placa} não encontrada na planilha de veículos para atualização de status.', 'warning')

        # Atualizar o agendamento para "Em Uso"
        try:
            agendamentos_sheet.update_cell(agendamento_row, 11, 'Em Uso')  # Status
            agendamentos_sheet.update_cell(agendamento_row, 15, agora.strftime('%d/%m/%Y %H:%M'))  # UltimaAtualizacao
        except Exception as e:
            flash(f'AVISO: Não foi possível atualizar o status do agendamento {agendamento_id}.', 'warning')

        flash('Saída registrada com sucesso!', 'success')
        return redirect(url_for('cronograma'))
    except Exception as e:
        print(f"ERRO ao registrar saída: {e}")  # Log para debug
        flash(f'Erro ao registrar saída: {e}', 'danger')
        return redirect(url_for('index'))

@app.route('/chegada')
@admin_required
def chegada():
    veiculos_em_uso = [v for v in veiculos_sheet.get_all_records() if v['Status'] == 'Em Uso']
    placa_pref = request.args.get('placa')
    return render_template('registrar_chegada.html', veiculos_em_uso=veiculos_em_uso, placa_pref=placa_pref)

@app.route('/registrar-chegada', methods=['POST'])
@admin_required
def registrar_chegada():
    placa = request.form.get('veiculo')
    km_final_str = request.form.get('km_final')
    
    # SUGESTÃO 1: VALIDAÇÃO DE DADOS
    km_final = int(km_final_str)
    km_inicial = -1
    viagem_a_finalizar_row = -1

    viagens_cells = viagens_sheet.findall(placa)
    for cell in reversed(viagens_cells):
        row_data = viagens_sheet.row_values(cell.row)
        if row_data[10] == 'Em Rota': # Coluna 11 (K) é o Status
            km_inicial = int(row_data[3]) # Coluna 4 (D) é KmInicial
            viagem_a_finalizar_row = cell.row
            break
            
    if km_inicial == -1:
        flash(f'Erro: Nenhuma viagem em rota encontrada para a placa {placa}.', 'danger')
        return redirect(url_for('chegada'))

    if km_final <= km_inicial:
        flash(f'Erro: A quilometragem final ({km_final} km) deve ser maior que a inicial ({km_inicial} km).', 'danger')
        return redirect(url_for('chegada'))

    # Se a validação passou, continua com o registro
    fuso_horario_sp = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(fuso_horario_sp)
    data_chegada = agora.strftime('%d/%m/%Y')
    hora_chegada = agora.strftime('%H:%M:%S')

    viagens_sheet.update_cell(viagem_a_finalizar_row, 5, km_final)
    viagens_sheet.update_cell(viagem_a_finalizar_row, 8, data_chegada)
    viagens_sheet.update_cell(viagem_a_finalizar_row, 9, hora_chegada)
    viagens_sheet.update_cell(viagem_a_finalizar_row, 11, "Finalizada")

    try:
        cell_veiculo = veiculos_sheet.find(placa)
        veiculos_sheet.update_cell(cell_veiculo.row, 4, "Disponível")
    except Exception as e:
        flash(f'AVISO: Placa {placa} não encontrada para liberar o status.', 'warning')

    # Atualizar agendamento correspondente para "Realizado"
    try:
        ag_list = agendamentos_sheet.get_all_records()
        ag_row_to_update = None
        for idx, a in enumerate(ag_list, 2):
            if a.get('PlacaVeiculo') == placa and a.get('Status') == 'Em Uso':
                ag_row_to_update = idx
                break
        if ag_row_to_update:
            agendamentos_sheet.update_cell(ag_row_to_update, 11, 'Realizado')
            agendamentos_sheet.update_cell(ag_row_to_update, 15, datetime.now(pytz.timezone("America/Sao_Paulo")).strftime('%d/%m/%Y %H:%M'))
    except Exception as e:
        pass
    
    flash('Chegada registrada com sucesso!', 'success')
    return redirect(url_for('index'))

# --- PÁGINAS DE VISUALIZAÇÃO ---

@app.route('/cronograma')
@login_required
def cronograma():
    viagens_em_rota = [v for v in get_all_records(viagens_sheet) if v['Status'] == 'Em Rota']
    
    # Buscar todos os agendamentos para cruzar informações
    agendamentos_list = agendamentos_sheet.get_all_records()
    usuarios_list = usuarios_sheet.get_all_records()
    
    # Enriquecer os dados com informações adicionais
    for viagem in viagens_em_rota:
        # Garantir que todos os campos existem, mesmo que vazios
        if 'Passageiros' not in viagem:
            viagem['Passageiros'] = '0'
        if 'Observacoes' not in viagem:
            viagem['Observacoes'] = ''
        if 'HoraChegada' not in viagem:
            viagem['HoraChegada'] = ''
        
        # Extrair ID do agendamento das observações
        obs = viagem.get('Observacoes', '')
        agendamento_id = None
        if '[Agendamento ID:' in obs:
            try:
                agendamento_id = obs.split('[Agendamento ID:')[1].split(']')[0].strip()
            except:
                pass
        
        # Buscar informações do agendamento e do usuário que fez
        if agendamento_id:
            for agend in agendamentos_list:
                if str(agend.get('ID')) == str(agendamento_id):
                    # Prioriza extrair o usuário que AGENDOU (não o motorista) das observações do admin
                    obs_admin = agend.get('Observacoes_Admin', '') or ''
                    agendado_por_username = None

                    if 'Agendado por:' in obs_admin:
                        try:
                            agendado_por_username = obs_admin.split('Agendado por:')[1].split(')')[0].strip()
                        except Exception:
                            agendado_por_username = None

                    # Caso no futuro exista uma coluna específica, usa como fallback
                    if not agendado_por_username:
                        agendado_por_username = agend.get('AgendadoPor') or agend.get('Usuario')

                    if agendado_por_username:
                        viagem['AgendadoPor'] = agendado_por_username
                        # Buscar telefone do usuário que agendou
                        for usuario in usuarios_list:
                            if str(usuario.get('username')) == str(agendado_por_username):
                                viagem['TelefoneContato'] = usuario.get('telefone', 'Não informado')
                                break
                    else:
                        # Não conseguiu identificar quem agendou; mantém campo vazio para não exibir
                        viagem['AgendadoPor'] = ''
                    break
    
    return render_template('cronograma.html', viagens=viagens_em_rota)

@app.route('/cancelar-viagem', methods=['POST'])
@admin_required
def cancelar_viagem():
    """Cancela uma viagem agendada (apenas para admin)."""
    try:
        viagem_id = request.form.get('viagem_id')
        
        if not viagem_id:
            flash('ID da viagem não fornecido.', 'danger')
            return redirect(url_for('cronograma'))
        
        # Encontrar a viagem com o ID e atualizar seu status
        viagens_records = viagens_sheet.get_all_records()
        viagem_encontrada = False
        
        for idx, viagem in enumerate(viagens_records, 2):  # Começa da linha 2
            if str(viagem.get('ID')) == str(viagem_id):
                # Atualizar o status para "Cancelada"
                viagens_sheet.update_cell(idx, 11, "Cancelada")  # Coluna 11 é Status
                viagem_encontrada = True
                
                # Liberar o veículo se estava em uso
                placa = viagem.get('PlacaVeiculo')
                if placa:
                    try:
                        cell = veiculos_sheet.find(placa)
                        veiculos_sheet.update_cell(cell.row, 4, "Disponível")
                    except:
                        pass
                
                break
        
        if viagem_encontrada:
            flash('Viagem cancelada com sucesso!', 'success')
        else:
            flash('Viagem não encontrada.', 'danger')
        
        return redirect(url_for('cronograma'))
    except Exception as e:
        print(f"ERRO ao cancelar viagem: {e}")
        flash(f'Erro ao cancelar viagem: {e}', 'danger')
        return redirect(url_for('cronograma'))

@app.route('/historico')
@admin_required
def historico():
    viagens_finalizadas = [v for v in get_all_records(viagens_sheet) if v['Status'] == 'Finalizada']
    return render_template('historico.html', viagens=viagens_finalizadas)

# --- ROTAS DE ADMIN (PROTEGIDAS E COM VERIFICAÇÃO DE PAPEL) ---

# --- PÁGINA DE GERENCIAMENTO ---

@app.route('/gerenciar')
@admin_required
def gerenciar():
    """Página para gerenciar motoristas, veículos E USUÁRIOS."""
    motoristas = motoristas_sheet.get_all_records()
    veiculos = veiculos_sheet.get_all_records()
    usuarios = usuarios_sheet.get_all_records()
    return render_template('gerenciar.html', motoristas=motoristas, veiculos=veiculos, usuarios=usuarios)


@app.route('/relatorios')
@admin_required
def relatorios():
    """
    Exibe um relatório diário de KM por veículo e por motorista.
    Permite a consulta de dias anteriores através de um parâmetro na URL.
    """
    # --- LÓGICA DE DATA ---
    # Pega a data da URL (formato YYYY-MM-DD)
    data_str = request.args.get('data')
    
    if data_str:
        try:
            data_selecionada_obj = datetime.strptime(data_str, '%Y-%m-%d').date()
        except ValueError:
            # Se a data for inválida, usa a data de hoje
            data_selecionada_obj = datetime.now().date()
            flash("Formato de data inválido. Exibindo relatório de hoje.", "warning")
    else:
        # Se nenhuma data for fornecida, usa a data de hoje
        data_selecionada_obj = datetime.now().date()

    # Formata a data para dois padrões:
    # 1. Para exibir no HTML (DD/MM/YYYY)
    data_display = data_selecionada_obj.strftime('%d/%m/%Y')
    # 2. Para comparar com os dados da planilha (que também é DD/MM/YYYY)
    data_comparacao = data_selecionada_obj.strftime('%d/%m/%Y')
    # 3. Para preencher o valor do input date no HTML (YYYY-MM-DD)
    data_input_value = data_selecionada_obj.strftime('%Y-%m-%d')

    # --- LÓGICA DE CÁLCULO ---
    viagens_finalizadas = [v for v in viagens_sheet.get_all_records() if v.get('Status') == 'Finalizada']
    
    # Filtra as viagens para incluir apenas as do dia selecionado (baseado na data de SAÍDA)
    viagens_do_dia = [v for v in viagens_finalizadas if v.get('DataSaida') == data_comparacao]
    
    relatorio_veiculos = {}
    relatorio_motoristas = {}

    for viagem in viagens_do_dia:
        try:
            km_inicial = int(viagem.get('KmInicial', 0))
            km_final = int(viagem.get('KmFinal', 0))
            
            # Garante que os dados são válidos para o cálculo
            if km_final > km_inicial:
                distancia = km_final - km_inicial
                
                # Acumula por veículo
                placa = viagem.get('PlacaVeiculo')
                if placa:
                    relatorio_veiculos[placa] = relatorio_veiculos.get(placa, 0) + distancia
                
                # Acumula por motorista
                motorista = viagem.get('Motorista')
                if motorista:
                    relatorio_motoristas[motorista] = relatorio_motoristas.get(motorista, 0) + distancia
        except (ValueError, TypeError):
            # Ignora linhas com KM inválido que não pode ser convertido para número
            continue
            
    return render_template('relatorios.html', 
                           relatorio_veiculos=relatorio_veiculos,
                           relatorio_motoristas=relatorio_motoristas,
                           data_display=data_display,
                           data_input_value=data_input_value)

# --- ROTAS DE AGENDAMENTO ---

@app.route('/agendamentos')
@login_required
def agendamentos():
    """Exibe lista de agendamentos do motorista ou todos (admin)."""
    agendamentos_list = agendamentos_sheet.get_all_records()
    # Filtros via querystring
    status_f = request.args.get('status', '').strip()
    placa_f = request.args.get('placa', '').strip()
    motorista_f = request.args.get('motorista', '').strip()
    data_de_f = request.args.get('data_de', '').strip()   # YYYY-MM-DD
    data_ate_f = request.args.get('data_ate', '').strip() # YYYY-MM-DD
    somente_ativos = request.args.get('somente_ativos', '').strip()  # '1' or ''

    # Aplicar filtros
    def parse_ddmmyyyy(s):
        try:
            return datetime.strptime(s, '%d/%m/%Y').date()
        except Exception:
            return None

    data_de = None
    data_ate = None
    try:
        if data_de_f:
            data_de = datetime.strptime(data_de_f, '%Y-%m-%d').date()
        if data_ate_f:
            data_ate = datetime.strptime(data_ate_f, '%Y-%m-%d').date()
    except Exception:
        data_de = None
        data_ate = None

    filtrados = []
    for ag in agendamentos_list:
        # Status
        if status_f and str(ag.get('Status', '')).strip() != status_f:
            continue
        # Placa
        if placa_f and placa_f.lower() not in str(ag.get('PlacaVeiculo', '')).lower():
            continue
        # Motorista (substring)
        if motorista_f and motorista_f.lower() not in str(ag.get('Motorista', '')).lower():
            continue
        # Intervalo de data solicitada
        ds = parse_ddmmyyyy(str(ag.get('DataSolicitada', '')))
        if data_de and (not ds or ds < data_de):
            continue
        if data_ate and (not ds or ds > data_ate):
            continue
        # Somente futuros/ativos: inclui 'Em Uso' sempre; inclui 'Agendado'/'Confirmado' com data de hoje ou futura; exclui 'Cancelado' e 'Realizado'
        if somente_ativos in ['1', 'on', 'true', 'True']:
            status_val = str(ag.get('Status', '')).strip()
            hoje = datetime.now().date()
            if status_val == 'Em Uso':
                pass  # sempre inclui
            elif status_val in ['Agendado', 'Confirmado']:
                if not ds or ds < hoje:
                    continue
            else:
                # Realizado, Cancelado ou qualquer outro status
                continue
        filtrados.append(ag)

    # Ordenação desejada:
    # 1) DataSolicitada ASC (próximos dias primeiro)
    # 2) Dentro do mesmo dia, ID DESC (agendamentos mais novos no topo)
    def id_int(item):
        try:
            return int(str(item.get('ID', '0')).strip())
        except Exception:
            return 0

    def data_solicitada(item):
        try:
            return datetime.strptime(item.get('DataSolicitada', ''), '%d/%m/%Y').date()
        except Exception:
            return datetime.max.date()

    filtrados.sort(key=lambda x: (data_solicitada(x), -id_int(x)))

    # Enriquecer com "AgendadoPor" e "TelefoneContato" (como no cronograma)
    try:
        usuarios_list = usuarios_sheet.get_all_records()
        for ag in filtrados:
            obs_admin = (ag.get('Observacoes_Admin') or '').strip()
            agendado_por_username = None

            if 'Agendado por:' in obs_admin:
                try:
                    agendado_por_username = obs_admin.split('Agendado por:')[1].split(')')[0].strip()
                except Exception:
                    agendado_por_username = None

            if not agendado_por_username:
                agendado_por_username = ag.get('AgendadoPor') or ag.get('Usuario')

            if agendado_por_username:
                ag['AgendadoPor'] = agendado_por_username
                for usuario in usuarios_list:
                    if str(usuario.get('username')) == str(agendado_por_username):
                        ag['TelefoneContato'] = usuario.get('telefone', 'Não informado')
                        break
    except Exception:
        pass
    
    return render_template('agendamentos.html', agendamentos=filtrados,
                           status_f=status_f, placa_f=placa_f, motorista_f=motorista_f,
                           data_de_f=data_de_f, data_ate_f=data_ate_f, somente_ativos=somente_ativos)

@app.route('/agendar-veiculo', methods=['GET', 'POST'])
@login_required
def agendar_veiculo():
    """Página para agendar um veículo."""
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            placa = request.form.get('veiculo')
            motorista_selecionado = request.form.get('motorista')
            data_solicitada = request.form.get('data_solicitada')
            hora_inicio = request.form.get('hora_inicio')
            hora_fim = request.form.get('hora_fim')
            destinos = request.form.get('destinos')
            passageiros = request.form.get('passageiros', '1')
            observacoes = request.form.get('observacoes', '')
            
            # Validações
            if not placa or not motorista_selecionado or not data_solicitada or not hora_inicio or not hora_fim or not destinos:
                flash('Todos os campos obrigatórios devem ser preenchidos.', 'danger')
                return redirect(url_for('agendar_veiculo'))
            
            # Validar se a data é futura
            try:
                data_obj = datetime.strptime(data_solicitada, '%Y-%m-%d').date()
                if data_obj < datetime.now().date():
                    flash('Não é possível agendar para datas passadas.', 'danger')
                    return redirect(url_for('agendar_veiculo'))
                data_formatada = data_obj.strftime('%d/%m/%Y')
            except:
                flash('Formato de data inválido.', 'danger')
                return redirect(url_for('agendar_veiculo'))
            
            # Validar hora
            if hora_inicio >= hora_fim:
                flash('A hora de início deve ser antes da hora de fim.', 'danger')
                return redirect(url_for('agendar_veiculo'))
            
            # Verificar se veículo existe
            veiculos = veiculos_sheet.get_all_records()
            veiculo_existe = any(v.get('Placa') == placa for v in veiculos)
            if not veiculo_existe:
                flash('Veículo não encontrado.', 'danger')
                return redirect(url_for('agendar_veiculo'))
            
            # Verificar conflitos de agendamento
            agendamentos_list = agendamentos_sheet.get_all_records()
            for agend in agendamentos_list:
                if (agend.get('PlacaVeiculo') == placa and 
                    agend.get('DataSolicitada') == data_formatada and
                    agend.get('Status') in ['Agendado', 'Confirmado', 'Em Uso']):
                    
                    # Verificar se horários se sobrepõem
                    inicio_existe = agend.get('HoraInicio', '')
                    fim_existe = agend.get('HoraFim', '')
                    
                    if not (hora_fim <= inicio_existe or hora_inicio >= fim_existe):
                        flash(f'Conflito de horário! Este veículo já está agendado para {data_formatada} entre {inicio_existe} e {fim_existe}.', 'danger')
                        return redirect(url_for('agendar_veiculo'))
            
            # Gerar novo ID
            novo_id = len(agendamentos_list) + 1
            data_agora = datetime.now().strftime('%d/%m/%Y')
            hora_agora = datetime.now().strftime('%H:%M')
            
            # Criar novo agendamento - usar motorista selecionado
            motorista = motorista_selecionado
            
            # Inclui no campo Observacoes_Admin quem fez o agendamento (username)
            observacoes_admin = f'Novo agendamento (Agendado por: {current_user.id})'

            novo_agendamento = [
                str(novo_id),                          # ID
                data_agora,                             # DataAgendamento
                motorista,                              # Motorista
                placa,                                  # PlacaVeiculo
                data_formatada,                         # DataSolicitada
                hora_inicio,                            # HoraInicio
                hora_fim,                               # HoraFim
                destinos,                               # Destinos
                passageiros,                            # Passageiros
                observacoes,                            # Observacoes
                'Agendado',                             # Status
                '',                                     # MotivoCancelamento
                '',                                     # DataCancelamento
                observacoes_admin,                      # Observacoes_Admin
                f'{data_agora} {hora_agora}'            # UltimaAtualizacao
            ]
            
            agendamentos_sheet.append_row(novo_agendamento)
            flash('Veículo agendado com sucesso!', 'success')
            return redirect(url_for('agendamentos'))
            
        except Exception as e:
            print(f"ERRO ao agendar veículo: {e}")
            flash(f'Erro ao agendar: {e}', 'danger')
            return redirect(url_for('agendar_veiculo'))
    
    # GET: Mostrar formulário
    veiculos = veiculos_sheet.get_all_records()
    motoristas = motoristas_sheet.get_all_records()  # Buscar todos os motoristas para seleção
    
    # Data mínima = amanhã
    data_minima = (datetime.now() + __import__('datetime').timedelta(days=1)).strftime('%Y-%m-%d')
    
    return render_template('agendar_veiculo.html', 
                         veiculos=veiculos, 
                         motoristas=motoristas,
                         data_minima=data_minima)

@app.route('/confirmar-agendamento/<agendamento_id>', methods=['POST'])
@admin_required
def confirmar_agendamento(agendamento_id):
    """Admin confirma um agendamento."""
    try:
        agendamentos_list = agendamentos_sheet.get_all_records()
        
        for idx, agend in enumerate(agendamentos_list, 2):
            if str(agend.get('ID')) == str(agendamento_id):
                data_agora = datetime.now().strftime('%d/%m/%Y %H:%M')
                agendamentos_sheet.update_cell(idx, 11, 'Confirmado')  # Status
                agendamentos_sheet.update_cell(idx, 15, data_agora)     # UltimaAtualizacao
                flash('Agendamento confirmado com sucesso!', 'success')
                break
        else:
            flash('Agendamento não encontrado.', 'danger')
    except Exception as e:
        print(f"ERRO ao confirmar agendamento: {e}")
        flash(f'Erro ao confirmar: {e}', 'danger')
    
    return redirect(url_for('agendamentos'))

@app.route('/cancelar-agendamento/<agendamento_id>', methods=['POST'])
@login_required
def cancelar_agendamento(agendamento_id):
    """Cancela um agendamento (motorista ou admin)."""
    try:
        motivo = request.form.get('motivo_cancelamento', '')
        agendamentos_list = agendamentos_sheet.get_all_records()
        
        for idx, agend in enumerate(agendamentos_list, 2):
            if str(agend.get('ID')) == str(agendamento_id):
                # Verificar permissão
                if current_user.role != 'admin' and agend.get('Motorista') != current_user.id:
                    flash('Você não tem permissão para cancelar este agendamento.', 'danger')
                    return redirect(url_for('agendamentos'))
                
                data_agora = datetime.now().strftime('%d/%m/%Y %H:%M')
                data_cancelamento = datetime.now().strftime('%d/%m/%Y')
                
                agendamentos_sheet.update_cell(idx, 11, 'Cancelado')           # Status
                agendamentos_sheet.update_cell(idx, 12, motivo)                # MotivoCancelamento
                agendamentos_sheet.update_cell(idx, 13, data_cancelamento)     # DataCancelamento
                agendamentos_sheet.update_cell(idx, 15, data_agora)            # UltimaAtualizacao
                
                flash('Agendamento cancelado com sucesso!', 'success')
                break
        else:
            flash('Agendamento não encontrado.', 'danger')
    except Exception as e:
        print(f"ERRO ao cancelar agendamento: {e}")
        flash(f'Erro ao cancelar: {e}', 'danger')
    
    return redirect(url_for('agendamentos'))

@app.route('/add-motorista', methods=['POST'])
@admin_required
def add_motorista():
    try:
        nome = request.form.get('nome')
        matricula = request.form.get('matricula')
        motoristas_sheet.append_row([nome, matricula])
        flash(f'Motorista {nome} adicionado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar motorista: {e}', 'danger')
    return redirect(url_for('gerenciar'))

@app.route('/add-veiculo', methods=['POST'])
@admin_required
def add_veiculo():
    try:
        modelo = request.form.get('modelo')
        placa = request.form.get('placa')
        ano = request.form.get('ano')
        veiculos_sheet.append_row([modelo, placa, ano, 'Disponível'])
        flash(f'Veículo {modelo} - {placa} adicionado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao adicionar veículo: {e}', 'danger')
    return redirect(url_for('gerenciar'))

@app.route('/add-user', methods=['POST'])
@admin_required
def add_user():
    """Processa o formulário de criação de novo usuário."""
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        telefone = request.form.get('telefone')
        role = request.form.get('role')

        # Verifica se o usuário já existe
        if User.get(username):
            flash(f'O nome de usuário "{username}" já existe. Tente outro.', 'danger')
            return redirect(url_for('gerenciar'))

        # Validação simples
        if not username or not password or not role or not telefone:
            flash('Todos os campos são obrigatórios.', 'danger')
            return redirect(url_for('gerenciar'))

        # Criptografa a senha
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Adiciona o novo usuário na planilha (com telefone na 4ª coluna)
        usuarios_sheet.append_row([username, password_hash, role, telefone])
        flash(f'Usuário {username} criado com sucesso!', 'success')

    except Exception as e:
        flash(f'Ocorreu um erro ao criar o usuário: {e}', 'danger')

    return redirect(url_for('gerenciar'))

# --- EXECUÇÃO DA APLICAÇÃO ---
if __name__ == '__main__':
    app.run(debug=True)