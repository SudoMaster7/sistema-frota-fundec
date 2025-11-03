# ⚡ Quick Reference - Agendamento e Cancelamento

## 🚀 Como Usar em 30 Segundos

### Agendar Saída (Qualquer Usuário)
```
1. "Registrar Saída" → 2. Escolha data/hora → 3. Preencha outros campos → 4. "Registrar"
```

### Cancelar Viagem (Apenas Admin)
```
1. "Cronograma" → 2. Clique "Cancelar" → 3. Confirme → ✅ Feito
```

---

## 📅 Campos Novos no Formulário

| Campo | Tipo | Padrão | Obrigatório |
|-------|------|--------|------------|
| Data da Saída | date | Hoje | ✅ Sim |
| Hora da Saída | time | (vazio) | ✅ Sim |

---

## 🎯 Botão de Cancelamento

**Onde**: Cronograma (um botão por viagem)  
**Quem vê**: Apenas admin  
**Cor**: Vermelho (perigo)  
**Ícone**: <i class="fa-solid fa-trash"></i>

---

## 📊 O Que Muda ao Cancelar

| Item | Antes | Depois |
|------|-------|--------|
| Status Viagem | "Em Rota" | "Cancelada" |
| Status Veículo | "Em Uso" | "Disponível" |
| No Cronograma | Visível | Desaparece |
| No Histórico | - | Aparece com "Cancelada" |

---

## 🔐 Permissões

```
Admin: ✅ Agendar, Cancelar
Motorista: ✅ Agendar (própria), ❌ Cancelar
```

---

## 💾 Arquivo de Logs

```
app.py (linha ~120):
- Captura data_saida_input e hora_saida_input
- Valida se foram preenchidos
- Usa valores no banco de dados

app.py (linha ~240):
- Rota /cancelar-viagem
- Valida permissão @admin_required
- Atualiza status e libera veículo
```

---

## 🧪 Teste Rápido

```bash
python teste_agendamento.py
```

Mostra:
- ✅ Conexão com planilha
- ✅ Estrutura de colunas
- ✅ Contagem de viagens por status
- ✅ Datas registradas

---

## 🎨 Design da Interface

### Campo de Data
```html
<input type="date" name="data_saida" required>
<!-- Abre calendário ao clicar -->
```

### Campo de Hora
```html
<input type="time" name="hora_saida" required>
<!-- Abre seletor de hora ao clicar -->
```

### Botão Cancelar
```html
<button class="btn btn-sm btn-danger" data-bs-target="#modal...">
    <i class="fa-solid fa-trash"></i>Cancelar
</button>
```

### Modal de Confirmação
```html
<div class="modal" id="modalCancelar...">
    <!-- Bootstrap modal com detalhes da viagem -->
    <!-- Botão de confirmação ao final -->
</div>
```

---

## 📝 Exemplos de Data/Hora

| Formato | Exemplo |
|---------|---------|
| Date Input | 2025-11-04 |
| Time Input | 14:30 |
| Armazenado BD | 04/11/2025 (DataSaida), 14:30 (HoraSaida) |

---

## ⚙️ Rotas Afetadas

| Rota | Mudança |
|------|---------|
| `/registrar-saida` POST | Agora usa data/hora do form |
| `/cronograma` GET | Mostra botão "Cancelar" para admin |
| `/cancelar-viagem` POST | **NOVA** - Cancela viagem |

---

## 🔄 Fluxo de Dados

```
Form (data_saida, hora_saida)
    ↓
request.form.get()
    ↓
nova_viagem[] (com data/hora)
    ↓
viagens_sheet.append_row()
    ↓
Google Sheets DB_Viagens
    ↓
Cronograma (exibe com data/hora)
```

---

## ✨ Validações

- ✅ Data e hora obrigatórias
- ✅ Admin obrigatório para cancelar
- ✅ Viagem ID validada ao cancelar
- ✅ Veículo liberado após cancelamento

---

## 🐛 Debugging

Se algo não funcionar:

```python
# No terminal Flask, procure por:
"ERRO ao registrar saída: ..."    # Registrar saída
"ERRO ao cancelar viagem: ..."     # Cancelar viagem

# Limpar cache:
Ctrl+Shift+Del (Firefox/Chrome)
```

---

## 📱 Responsividade

- Desktop: ✅ Funciona perfeitamente
- Tablet: ✅ Adaptado
- Mobile: ✅ Layout empilhado

---

## 🎓 Documentação Completa

- `GUIA_AGENDAMENTO_CANCELAMENTO.md` - Manual completo
- `RESUMO_IMPLEMENTACAO.md` - Visão geral técnica
- Este arquivo - Quick reference

---

**Versão**: 1.1  
**Status**: ✅ Pronto para produção  
**Último update**: 03/11/2025
