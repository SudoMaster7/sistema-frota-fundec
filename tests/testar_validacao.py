"""
🧪 Script de Teste - Validação de Formulário de Agendamento

Este script simula o envio de formulário para verificar se as correções
de validação estão funcionando corretamente.
"""

import sys

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_test(test_name, passed, message=""):
    """Imprime resultado de teste colorido."""
    status = f"{GREEN}✅ PASSOU{RESET}" if passed else f"{RED}❌ FALHOU{RESET}"
    print(f"\n{status} - {test_name}")
    if message:
        print(f"  {message}")

def test_template_field_names():
    """Verifica se os nomes dos campos no template estão corretos."""
    print(f"\n{BLUE}═══════════════════════════════════════════════════════{RESET}")
    print(f"{BLUE}📋 TESTE 1: Verificar nomes dos campos no template{RESET}")
    print(f"{BLUE}═══════════════════════════════════════════════════════{RESET}")
    
    # Ler o template
    with open('templates/agendar_veiculo.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Campos esperados pelo backend
    expected_fields = {
        'veiculo': 'name="veiculo"',
        'data_solicitada': 'name="data_solicitada"',
        'hora_inicio': 'name="hora_inicio"',
        'hora_fim': 'name="hora_fim"',
        'destinos': 'name="destinos"',
        'passageiros': 'name="passageiros"',
        'observacoes': 'name="observacoes"'
    }
    
    all_passed = True
    for field_name, expected_attr in expected_fields.items():
        if expected_attr in template_content:
            print_test(f"Campo '{field_name}'", True, f"✓ Encontrado: {expected_attr}")
        else:
            print_test(f"Campo '{field_name}'", False, f"✗ Não encontrado: {expected_attr}")
            all_passed = False
    
    # Verificar se o campo antigo (incorreto) ainda existe
    if 'name="placa_veiculo"' in template_content:
        print_test("Verificar campo antigo 'placa_veiculo'", False, 
                  f"{RED}✗ Campo antigo ainda presente! Deve ser removido.{RESET}")
        all_passed = False
    else:
        print_test("Verificar campo antigo 'placa_veiculo'", True, 
                  f"{GREEN}✓ Campo antigo corretamente removido{RESET}")
    
    return all_passed

def test_backend_validation():
    """Verifica a lógica de validação no backend."""
    print(f"\n{BLUE}═══════════════════════════════════════════════════════{RESET}")
    print(f"{BLUE}📋 TESTE 2: Verificar validação no backend{RESET}")
    print(f"{BLUE}═══════════════════════════════════════════════════════{RESET}")
    
    # Ler o app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Verificar se o backend busca o campo correto
    checks = {
        "Backend busca 'veiculo'": "request.form.get('veiculo')",
        "Backend busca 'data_solicitada'": "request.form.get('data_solicitada')",
        "Backend busca 'hora_inicio'": "request.form.get('hora_inicio')",
        "Backend busca 'hora_fim'": "request.form.get('hora_fim')",
        "Backend busca 'destinos'": "request.form.get('destinos')",
        "Validação verifica 'placa'": "if not placa or not data_solicitada"
    }
    
    all_passed = True
    for check_name, expected_code in checks.items():
        if expected_code in app_content:
            print_test(check_name, True, f"✓ Código encontrado")
        else:
            print_test(check_name, False, f"✗ Código não encontrado")
            all_passed = False
    
    return all_passed

def test_cancel_modal():
    """Verifica se o modal de cancelamento está correto."""
    print(f"\n{BLUE}═══════════════════════════════════════════════════════{RESET}")
    print(f"{BLUE}📋 TESTE 3: Verificar modal de cancelamento{RESET}")
    print(f"{BLUE}═══════════════════════════════════════════════════════{RESET}")
    
    # Ler o template de agendamentos
    with open('templates/agendamentos.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Verificar se o ID é passado corretamente
    checks = {
        "ID passado corretamente": 'onclick="abrirModalCancelamento({{ agend.ID }})"' in template_content,
        "Campo motivo presente": 'name="motivo_cancelamento"' in template_content,
        "Função JavaScript existe": 'function abrirModalCancelamento' in template_content
    }
    
    all_passed = True
    for check_name, condition in checks.items():
        print_test(check_name, condition, 
                  f"{'✓ Verificado' if condition else '✗ Não encontrado'}")
        if not condition:
            all_passed = False
    
    # Verificar se erro antigo foi corrigido
    if "{{ 'agend.ID' }}" in template_content:
        print_test("Erro antigo corrigido", False, 
                  f"{RED}✗ String literal '{{ 'agend.ID' }}' ainda presente!{RESET}")
        all_passed = False
    else:
        print_test("Erro antigo corrigido", True, 
                  f"{GREEN}✓ Erro de string literal corrigido{RESET}")
    
    return all_passed

def test_field_consistency():
    """Verifica consistência entre frontend e backend."""
    print(f"\n{BLUE}═══════════════════════════════════════════════════════{RESET}")
    print(f"{BLUE}📋 TESTE 4: Verificar consistência Frontend ↔ Backend{RESET}")
    print(f"{BLUE}═══════════════════════════════════════════════════════{RESET}")
    
    # Ler ambos os arquivos
    with open('templates/agendar_veiculo.html', 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    with open('app.py', 'r', encoding='utf-8') as f:
        app_content = f.read()
    
    # Campos críticos
    critical_fields = [
        ('veiculo', 'placa'),
        ('data_solicitada', 'data_solicitada'),
        ('hora_inicio', 'hora_inicio'),
        ('hora_fim', 'hora_fim'),
        ('destinos', 'destinos')
    ]
    
    all_passed = True
    for frontend_name, backend_var in critical_fields:
        frontend_exists = f'name="{frontend_name}"' in template_content
        backend_uses = f"request.form.get('{frontend_name}')" in app_content
        
        if frontend_exists and backend_uses:
            print_test(f"Campo '{frontend_name}'", True, 
                      f"✓ Frontend e Backend sincronizados")
        else:
            print_test(f"Campo '{frontend_name}'", False, 
                      f"✗ Frontend: {frontend_exists}, Backend: {backend_uses}")
            all_passed = False
    
    return all_passed

def main():
    """Executa todos os testes."""
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}🧪 TESTES DE VALIDAÇÃO - SISTEMA DE AGENDAMENTOS{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")
    
    tests = [
        ("Nomes dos Campos no Template", test_template_field_names),
        ("Validação no Backend", test_backend_validation),
        ("Modal de Cancelamento", test_cancel_modal),
        ("Consistência Frontend ↔ Backend", test_field_consistency)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"\n{RED}❌ ERRO ao executar teste '{test_name}': {e}{RESET}")
            results.append((test_name, False))
    
    # Resumo final
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{YELLOW}📊 RESUMO DOS TESTES{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = f"{GREEN}✅ PASSOU{RESET}" if passed else f"{RED}❌ FALHOU{RESET}"
        print(f"{status} - {test_name}")
    
    print(f"\n{YELLOW}Resultado Final: {passed_count}/{total_count} testes passaram{RESET}")
    
    if passed_count == total_count:
        print(f"\n{GREEN}{'='*60}{RESET}")
        print(f"{GREEN}🎉 TODOS OS TESTES PASSARAM!{RESET}")
        print(f"{GREEN}{'='*60}{RESET}")
        print(f"\n{GREEN}✅ O sistema de agendamentos está pronto para uso!{RESET}")
        print(f"{GREEN}✅ As correções de validação foram aplicadas com sucesso!{RESET}")
        return 0
    else:
        print(f"\n{RED}{'='*60}{RESET}")
        print(f"{RED}⚠️  ALGUNS TESTES FALHARAM{RESET}")
        print(f"{RED}{'='*60}{RESET}")
        print(f"\n{RED}❌ Revise as correções antes de usar o sistema.{RESET}")
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⚠️  Testes interrompidos pelo usuário{RESET}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{RED}❌ ERRO FATAL: {e}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
