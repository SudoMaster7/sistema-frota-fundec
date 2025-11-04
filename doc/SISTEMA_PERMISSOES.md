# 🔐 SISTEMA DE PERMISSÕES - Frota FUNDEC

**Data:** 04/11/2025  
**Versão:** 1.3.0  
**Tipo:** Definição de Permissões e Controle de Acesso

---

## 👥 ROLES DO SISTEMA

O sistema possui 2 níveis de acesso:

### 1. **Usuário Comum** (Role: `user`)
- Usuários padrão do sistema
- Motoristas, secretárias, colaboradores
- Acesso limitado às funcionalidades básicas

### 2. **Administrador** (Role: `admin`)
- Gestores da frota
- Acesso total ao sistema
- Pode confirmar e gerenciar todos os agendamentos

---

## 📋 MATRIZ DE PERMISSÕES

### 🟢 Funcionalidades Acessíveis a TODOS os Usuários

| Funcionalidade | Usuário | Admin | Descrição |
|----------------|---------|-------|-----------|
| **Login/Logout** | ✅ | ✅ | Acesso ao sistema |
| **Ver Dashboard** | ✅ | ✅ | Visualizar resumo geral |
| **Ver Cronograma** | ✅ | ✅ | Ver veículos em rota em tempo real |
| **Registrar Saída** | ✅ | ✅ | Iniciar viagem com veículo |
| **Registrar Chegada** | ✅ | ✅ | Finalizar viagem |
| **Ver Histórico** | ✅ | ✅ | Consultar viagens passadas |
| **Ver Próprios Agendamentos** | ✅ | ✅ | Lista dos seus agendamentos |
| **Criar Agendamento** | ✅ | ✅ | Agendar veículo para uso futuro |
| **Cancelar Próprios Agendamentos** | ✅ | ✅ | Cancelar seus agendamentos |

### 🔴 Funcionalidades EXCLUSIVAS de Administrador

| Funcionalidade | Usuário | Admin | Descrição |
|----------------|---------|-------|-----------|
| **Ver Todos Agendamentos** | ❌ | ✅ | Ver agendamentos de todos os usuários |
| **Confirmar Agendamentos** | ❌ | ✅ | Aprovar agendamentos pendentes |
| **Cancelar Qualquer Agendamento** | ❌ | ✅ | Cancelar agendamentos de outros usuários |
| **Cancelar Viagem em Rota** | ❌ | ✅ | Cancelar viagem já iniciada |
| **Gerenciar Dados** | ❌ | ✅ | Adicionar veículos, motoristas |
| **Ver Relatórios** | ❌ | ✅ | Relatórios analíticos completos |

---

## 🔄 FLUXO DE AGENDAMENTO

### Para Usuários Comuns

```
1. USUÁRIO cria agendamento
   ↓
2. Status: "Agendado" (Pendente de Confirmação)
   ↓
3. ADMIN visualiza e confirma
   ↓
4. Status: "Confirmado"
   ↓
5. Na data/hora agendada → Usuário pode usar veículo
```

### Para Administradores

```
1. ADMIN cria agendamento
   ↓
2. Status: "Confirmado" (Confirmação automática)
   ↓
3. Na data/hora agendada → Veículo disponível
```

---

## 📊 ESTADOS DE AGENDAMENTO

| Status | Descrição | Quem Pode Ver | Quem Pode Modificar |
|--------|-----------|---------------|---------------------|
| **Agendado** | Aguardando confirmação do admin | Criador + Admin | Criador (cancelar) + Admin (confirmar/cancelar) |
| **Confirmado** | Aprovado pelo admin | Criador + Admin | Admin (cancelar) |
| **Em Uso** | Veículo sendo utilizado | Todos | Motorista (finalizar) + Admin (cancelar) |
| **Finalizado** | Uso concluído | Todos | Ninguém (histórico) |
| **Cancelado** | Agendamento cancelado | Criador + Admin | Ninguém (histórico) |

---

## 🎯 PERMISSÕES DETALHADAS

### 1. Ver Cronograma (`/cronograma`)

**Acesso:** ✅ Todos os usuários  
**Decorator:** `@login_required`

**O que vê:**
- Todos os veículos em rota
- Informações de motorista, destino, horários
- Status em tempo real

**Restrições:**
- Usuários comuns: apenas visualização
- Admin: visualização + poder de cancelar viagens

---

### 2. Criar Agendamento (`/agendar-veiculo`)

**Acesso:** ✅ Todos os usuários  
**Decorator:** `@login_required`

**Campos obrigatórios:**
- ✓ Veículo
- ✓ Motorista (seleção livre)
- ✓ Data solicitada (futura)
- ✓ Hora início e fim
- ✓ Destinos

**Comportamento:**
- **Usuários comuns:** Status inicial = "Agendado" (aguarda confirmação)
- **Admin:** Status inicial = "Confirmado" (aprovação automática)

**Validações aplicadas:**
- Data não pode ser passada
- Hora fim > hora início
- Verificação de conflitos de horário
- Veículo deve existir no sistema

---

### 3. Ver Agendamentos (`/agendamentos`)

**Acesso:** ✅ Todos os usuários  
**Decorator:** `@login_required`

**Comportamento:**
```python
if current_user.role != 'admin':
    # Usuário comum vê apenas SEUS agendamentos
    agendamentos_list = [a for a in agendamentos_list 
                        if a.get('Motorista') == current_user.id]
else:
    # Admin vê TODOS os agendamentos
    agendamentos_list = agendamentos_sheet.get_all_records()
```

**Informações exibidas:**
- Lista de agendamentos filtrada por permissão
- Status visual (badges coloridos)
- Botões de ação apropriados ao role

---

### 4. Confirmar Agendamento (`/confirmar-agendamento/<id>`)

**Acesso:** ❌ Apenas Administradores  
**Decorator:** `@admin_required`

**Ação:**
- Muda status de "Agendado" para "Confirmado"
- Registra data/hora da confirmação
- Envia feedback ao usuário

**Regras:**
- Apenas agendamentos com status "Agendado" podem ser confirmados
- Admin não precisa confirmar seus próprios agendamentos

---

### 5. Cancelar Agendamento (`/cancelar-agendamento/<id>`)

**Acesso:** ✅ Criador do agendamento OU Admin  
**Decorator:** `@login_required`

**Validação de permissão:**
```python
if current_user.role != 'admin' and agend.get('Motorista') != current_user.id:
    flash('Você não tem permissão para cancelar este agendamento.', 'danger')
    return redirect(url_for('agendamentos'))
```

**Comportamento:**
- **Usuário comum:** Pode cancelar apenas seus próprios agendamentos
- **Admin:** Pode cancelar qualquer agendamento
- Motivo do cancelamento é opcional

---

### 6. Cancelar Viagem (`/cancelar-viagem`)

**Acesso:** ❌ Apenas Administradores  
**Decorator:** `@admin_required`

**Ação:**
- Cancela viagem já em andamento
- Libera veículo para outros usos
- Registra motivo e responsável

**Quando usar:**
- Emergências
- Mudanças de plano
- Problemas mecânicos

---

### 7. Gerenciar Dados (`/gerenciar`)

**Acesso:** ❌ Apenas Administradores  
**Decorator:** `@admin_required`

**Funcionalidades:**
- Adicionar novos veículos
- Cadastrar motoristas
- Editar informações
- Excluir registros

---

### 8. Relatórios (`/relatorios`)

**Acesso:** ❌ Apenas Administradores  
**Decorator:** `@admin_required`

**Informações:**
- Estatísticas de uso
- Quilometragem total
- Ranking de motoristas
- Relatórios de manutenção

---

## 🎨 INDICADORES VISUAIS

### Badges de Role no Navbar

**Usuário Comum:**
```html
<span class="badge bg-info">
    <i class="fa-solid fa-user-check"></i> Usuário
</span>
```

**Administrador:**
```html
<span class="badge bg-danger">
    <i class="fa-solid fa-shield-halved"></i> Admin
</span>
```

### Avisos nas Páginas

**Página de Agendamentos (Usuário):**
```
ℹ️ Informações sobre Agendamentos
• Ver Cronograma: Você pode visualizar todos os veículos em uso
• Criar Agendamento: Você pode agendar veículos para datas futuras
• Aguardar Confirmação: Seus agendamentos precisam ser confirmados pelo administrador
• Cancelar: Você pode cancelar seus próprios agendamentos a qualquer momento
```

**Página de Agendamentos (Admin):**
```
🛡️ Permissões de Administrador
• Ver Todos: Você visualiza todos os agendamentos do sistema
• Confirmar: Você pode confirmar agendamentos pendentes
• Cancelar Qualquer: Você pode cancelar qualquer agendamento
• Criar Agendamento: Seus agendamentos são confirmados automaticamente
```

**Página de Cronograma (Todos):**
```
👁️ Acesso Permitido
Todos os usuários podem visualizar este cronograma em tempo real.
Para agendar um veículo, acesse Novo Agendamento.
```

---

## 🔐 IMPLEMENTAÇÃO TÉCNICA

### Decorator `@admin_required`

```python
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Acesso negado. Área restrita a administradores.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
```

### Verificação de Role no Template

```jinja2
{% if current_user.role == 'admin' %}
    <!-- Conteúdo exclusivo para admin -->
    <button>Confirmar Agendamento</button>
{% else %}
    <!-- Conteúdo para usuários comuns -->
    <p>Aguardando confirmação do administrador</p>
{% endif %}
```

### Filtragem de Dados por Permissão

```python
# Na rota /agendamentos
agendamentos_list = agendamentos_sheet.get_all_records()

if current_user.role != 'admin':
    # Filtrar apenas agendamentos do usuário
    agendamentos_list = [a for a in agendamentos_list 
                        if a.get('Motorista') == current_user.id]
```

---

## 📝 MENSAGENS DE ERRO

### Acesso Negado
```
"Acesso negado. Área restrita a administradores."
```

### Sem Permissão para Cancelar
```
"Você não tem permissão para cancelar este agendamento."
```

### Agendamento não Encontrado
```
"Agendamento não encontrado."
```

---

## 🧪 COMO TESTAR

### 1. Testar como Usuário Comum

```bash
# Login como usuário normal
# Navegue e verifique:
- ✅ Pode ver cronograma
- ✅ Pode criar agendamento (status: Agendado)
- ✅ Vê apenas seus agendamentos
- ✅ Pode cancelar seus agendamentos
- ❌ NÃO vê menu "Gerenciar"
- ❌ NÃO vê menu "Relatórios"
- ❌ NÃO pode confirmar agendamentos
- ❌ NÃO pode cancelar viagens em rota
```

### 2. Testar como Administrador

```bash
# Login como admin
# Navegue e verifique:
- ✅ Pode ver cronograma
- ✅ Pode criar agendamento (status: Confirmado)
- ✅ Vê TODOS os agendamentos
- ✅ Pode confirmar agendamentos pendentes
- ✅ Pode cancelar qualquer agendamento
- ✅ Vê menu "Gerenciar"
- ✅ Vê menu "Relatórios"
- ✅ Pode cancelar viagens em rota
```

---

## 🎯 CASOS DE USO

### Caso 1: Usuário Agenda Veículo

**Cenário:**
Maria (usuária comum) precisa de um veículo para amanhã.

**Fluxo:**
1. Maria acessa `/agendar-veiculo`
2. Preenche: veículo, motorista, data, horários, destino
3. Clica em "Agendar Veículo"
4. Status: **"Agendado"** (aguardando confirmação)
5. Admin recebe notificação visual na lista
6. Admin confirma o agendamento
7. Status muda para **"Confirmado"**
8. Maria pode usar o veículo no dia agendado

---

### Caso 2: Admin Agenda Veículo

**Cenário:**
João (admin) precisa de um veículo urgente.

**Fluxo:**
1. João acessa `/agendar-veiculo`
2. Preenche os dados do agendamento
3. Clica em "Agendar Veículo"
4. Status: **"Confirmado"** (aprovação automática)
5. João pode usar imediatamente na data agendada

---

### Caso 3: Usuário Tenta Cancelar Agendamento de Outro

**Cenário:**
Maria tenta cancelar agendamento de Pedro.

**Fluxo:**
1. Maria acessa `/agendamentos`
2. **Não vê** agendamentos de Pedro (filtro por usuário)
3. Se tentar acessar URL direta: `/cancelar-agendamento/123`
4. Sistema verifica: `current_user.id != agendamento.motorista`
5. Bloqueia ação: "Você não tem permissão para cancelar este agendamento."

---

### Caso 4: Admin Confirma Múltiplos Agendamentos

**Cenário:**
Admin tem 10 agendamentos pendentes.

**Fluxo:**
1. Admin acessa `/agendamentos`
2. Vê TODOS os 10 agendamentos
3. Identifica os com status "Agendado"
4. Clica em "Confirmar" em cada um
5. Status muda para "Confirmado"
6. Usuários recebem feedback visual

---

## 📊 ESTATÍSTICAS DE PERMISSÃO

| Métrica | Valor |
|---------|-------|
| Total de Rotas Protegidas | 15+ |
| Rotas Públicas | 1 (login) |
| Rotas para Todos Usuários | 8 |
| Rotas Exclusivas Admin | 6 |
| Decorators Implementados | 2 (`@login_required`, `@admin_required`) |
| Verificações de Permissão | 12+ |

---

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

- [x] Decorator `@admin_required` criado
- [x] Rotas protegidas com decorators apropriados
- [x] Filtragem de agendamentos por usuário
- [x] Verificação de permissão em cancelamentos
- [x] Badges de role no navbar
- [x] Avisos informativos em páginas
- [x] Menu condicional para admin
- [x] Status visual de agendamentos
- [x] Confirmação automática para admin
- [x] Mensagens de erro apropriadas

---

## 🔄 PRÓXIMAS MELHORIAS

- [ ] Sistema de notificações (email/push)
- [ ] Histórico de ações (audit log)
- [ ] Permissões granulares (roles customizados)
- [ ] Aprovação em múltiplos níveis
- [ ] Dashboard específico por role
- [ ] Relatórios personalizados por usuário

---

**Status:** ✅ **IMPLEMENTADO E TESTADO**  
**Pronto para produção:** Sim  
**Documentação completa:** Sim

---

*Documento criado em 04/11/2025*
