"""
Teste do Sistema de Agendamentos
Valida a lógica de conflito de horários e funcionalidades do agendamento
"""

from datetime import datetime, timedelta

def validar_conflito_horario(hora_inicio_novo, hora_fim_novo, hora_inicio_existente, hora_fim_existente):
    """
    Verifica se há conflito entre dois agendamentos.
    Retorna True se há conflito, False caso contrário.
    """
    # Converte strings HH:MM para minutos desde meia-noite
    def horas_para_minutos(hora_str):
        h, m = map(int, hora_str.split(':'))
        return h * 60 + m
    
    inicio_novo = horas_para_minutos(hora_inicio_novo)
    fim_novo = horas_para_minutos(hora_fim_novo)
    inicio_exist = horas_para_minutos(hora_inicio_existente)
    fim_exist = horas_para_minutos(hora_fim_existente)
    
    # Não há conflito se: fim_novo <= inicio_exist OU inicio_novo >= fim_exist
    # Logo, há conflito se NÃO for nenhum dos dois casos acima
    return not (fim_novo <= inicio_exist or inicio_novo >= fim_exist)

def testar_conflitos():
    """Testa a lógica de detecção de conflitos."""
    print("=" * 60)
    print("🧪 TESTES DE DETECÇÃO DE CONFLITO DE HORÁRIOS")
    print("=" * 60)
    
    casos_teste = [
        {
            "nome": "Sem conflito: horários não se sobrepõem",
            "novo": ("08:00", "12:00"),
            "existente": ("13:00", "17:00"),
            "esperado": False
        },
        {
            "nome": "Sem conflito: horários adjacentes",
            "novo": ("08:00", "12:00"),
            "existente": ("12:00", "16:00"),
            "esperado": False
        },
        {
            "nome": "Conflito: horários parcialmente sobrepostos",
            "novo": ("11:00", "15:00"),
            "existente": ("08:00", "12:00"),
            "esperado": True
        },
        {
            "nome": "Conflito: novo agendamento dentro do existente",
            "novo": ("09:00", "11:00"),
            "existente": ("08:00", "12:00"),
            "esperado": True
        },
        {
            "nome": "Conflito: novo agendamento contém o existente",
            "novo": ("07:00", "13:00"),
            "existente": ("08:00", "12:00"),
            "esperado": True
        },
        {
            "nome": "Conflito: mesmos horários exatos",
            "novo": ("08:00", "12:00"),
            "existente": ("08:00", "12:00"),
            "esperado": True
        },
        {
            "nome": "Sem conflito: horários invertidos (inválido)",
            "novo": ("15:00", "12:00"),
            "existente": ("08:00", "12:00"),
            "esperado": False  # Tecnicamente inválido, mas sem conflito por comparação
        },
    ]
    
    testes_passaram = 0
    testes_falharam = 0
    
    for i, caso in enumerate(casos_teste, 1):
        inicio_novo, fim_novo = caso["novo"]
        inicio_exist, fim_exist = caso["existente"]
        resultado = validar_conflito_horario(inicio_novo, fim_novo, inicio_exist, fim_exist)
        esperado = caso["esperado"]
        
        passou = resultado == esperado
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        testes_passaram += passou
        testes_falharam += not passou
        
        print(f"\nTeste {i}: {status}")
        print(f"  Descrição: {caso['nome']}")
        print(f"  Novo agendamento: {inicio_novo} - {fim_novo}")
        print(f"  Agendamento existente: {inicio_exist} - {fim_exist}")
        print(f"  Resultado: Conflito={resultado}, Esperado={esperado}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO: {testes_passaram} passaram, {testes_falharam} falharam")
    print("=" * 60)
    
    return testes_falharam == 0

def testar_validacoes_data():
    """Testa validações de data."""
    print("\n" + "=" * 60)
    print("🧪 TESTES DE VALIDAÇÃO DE DATA")
    print("=" * 60)
    
    hoje = datetime.now().date()
    amanha = hoje + timedelta(days=1)
    ontem = hoje - timedelta(days=1)
    
    casos_teste = [
        {
            "nome": "Data válida: amanhã",
            "data": amanha.strftime('%Y-%m-%d'),
            "esperado": True
        },
        {
            "nome": "Data válida: daqui a 30 dias",
            "data": (hoje + timedelta(days=30)).strftime('%Y-%m-%d'),
            "esperado": True
        },
        {
            "nome": "Data inválida: ontem",
            "data": ontem.strftime('%Y-%m-%d'),
            "esperado": False
        },
        {
            "nome": "Data inválida: hoje",
            "data": hoje.strftime('%Y-%m-%d'),
            "esperado": False
        },
    ]
    
    testes_passaram = 0
    
    for i, caso in enumerate(casos_teste, 1):
        data_obj = datetime.strptime(caso["data"], '%Y-%m-%d').date()
        resultado = data_obj > hoje  # Data deve ser FUTURA (não pode ser hoje)
        esperado = caso["esperado"]
        
        passou = resultado == esperado
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        testes_passaram += passou
        
        print(f"\nTeste {i}: {status}")
        print(f"  Descrição: {caso['nome']}")
        print(f"  Data: {caso['data']} (hoje: {hoje})")
        print(f"  Resultado: Válida={resultado}, Esperado={esperado}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO: {testes_passaram}/{len(casos_teste)} testes passaram")
    print("=" * 60)
    
    return testes_passaram == len(casos_teste)

def testar_validacoes_hora():
    """Testa validações de hora."""
    print("\n" + "=" * 60)
    print("🧪 TESTES DE VALIDAÇÃO DE HORA")
    print("=" * 60)
    
    casos_teste = [
        {
            "nome": "Horário válido: início antes do fim",
            "inicio": "08:00",
            "fim": "17:00",
            "esperado": True
        },
        {
            "nome": "Horário inválido: início = fim",
            "inicio": "08:00",
            "fim": "08:00",
            "esperado": False
        },
        {
            "nome": "Horário inválido: início depois do fim",
            "inicio": "17:00",
            "fim": "08:00",
            "esperado": False
        },
        {
            "nome": "Horário válido: diferença de 1 minuto",
            "inicio": "08:00",
            "fim": "08:01",
            "esperado": True
        },
    ]
    
    testes_passaram = 0
    
    for i, caso in enumerate(casos_teste, 1):
        resultado = caso["inicio"] < caso["fim"]  # Deve ser menor (fim > inicio)
        esperado = caso["esperado"]
        
        passou = resultado == esperado
        status = "✅ PASSOU" if passou else "❌ FALHOU"
        testes_passaram += passou
        
        print(f"\nTeste {i}: {status}")
        print(f"  Descrição: {caso['nome']}")
        print(f"  Hora Início: {caso['inicio']}, Hora Fim: {caso['fim']}")
        print(f"  Resultado: Válido={resultado}, Esperado={esperado}")
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO: {testes_passaram}/{len(casos_teste)} testes passaram")
    print("=" * 60)
    
    return testes_passaram == len(casos_teste)

if __name__ == '__main__':
    print("\n")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║     TESTES DO SISTEMA DE AGENDAMENTOS DE VEÍCULOS         ║")
    print("╚════════════════════════════════════════════════════════════╝")
    
    resultado1 = testar_conflitos()
    resultado2 = testar_validacoes_data()
    resultado3 = testar_validacoes_hora()
    
    print("\n" + "=" * 60)
    if resultado1 and resultado2 and resultado3:
        print("🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM - VERIFIQUE OS RESULTADOS ACIMA")
    print("=" * 60 + "\n")
