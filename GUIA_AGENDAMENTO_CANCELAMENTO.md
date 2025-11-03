# 📅 Guia - Novas Funcionalidades: Agendamento de Saídas e Cancelamento

## ✨ Novas Funcionalidades Implementadas

### 1. **Agendamento de Data e Hora de Saída** 📆🕐

Agora é possível agendar a saída de um veículo para **qualquer data e horário no futuro**.

#### Como Usar:
1. Acesse **"Registrar Saída"**
2. Preencha o formulário normalmente
3. **NOVO**: Escolha a **Data da Saída** (calendário com datepicker)
4. **NOVO**: Escolha a **Hora da Saída** (relógio com time picker)
5. Os outros campos permanecem os mesmos
6. Clique em "Registrar Saída"

#### Detalhes:
- 📌 A data é **preenchida automaticamente com o dia de hoje**
- 📌 Você pode escolher **qualquer data futura**
- 📌 O horário pode ser definido de forma livre
- 📌 O sistema **não bloqueia saídas agendadas para o passado** (para flexibilidade)

#### Exemplo de Uso:
```
Motorista: João Silva
Veículo: ABC-1234
Data: 05/11/2025 (próxima segunda)
Hora: 14:30
KM Inicial: 85420
Passageiros: 3
Destinos: Centro, Filial Sul
```

---

### 2. **Cancelamento de Viagens** ❌ (Apenas Admin)

O **administrador** pode cancelar viagens diretamente do cronograma.

#### Como Usar:
1. Acesse a página **"Cronograma"**
2. Localize a viagem desejada
3. Clique no botão **"Cancelar"** (apenas apareça para admin)
4. Uma janela de confirmação abrirá
5. Confirme o cancelamento

#### O Que Acontece Ao Cancelar:
- ✅ A viagem muda de status para **"Cancelada"**
- ✅ O veículo muda de **"Em Uso"** para **"Disponível"**
- ✅ Uma mensagem de sucesso aparece
- ✅ A viagem desaparece do cronograma

#### Modal de Confirmação:
```
┌──────────────────────────────────┐
│ ⚠️  CANCELAR VIAGEM               │
├──────────────────────────────────┤
│ Tem certeza que deseja cancelar?  │
│                                  │
│ Veículo: ABC-1234                │
│ Motorista: João Silva            │
│ Data/Hora: 05/11/2025 às 14:30  │
│                                  │
│ ⚠️ Esta ação não pode ser desfeita!
│                                  │
│ [Não, Voltar] [Sim, Cancelar]   │
└──────────────────────────────────┘
```

---

## 🔄 Fluxo de Funcionamento

### Cenário 1: Registrar Saída para Hoje
```
1. Admin/Motorista clica em "Registrar Saída"
2. Sistema preenche data com hoje automaticamente
3. Escolhe hora desejada
4. Preenche outros dados
5. Clica em "Registrar"
6. Viagem aparece em "Cronograma" como "Em Rota"
7. Motorista segue com o trajeto
8. Ao voltar, acessa "Registrar Chegada" e finaliza
```

### Cenário 2: Agendar Saída para Amanhã
```
1. Admin clica em "Registrar Saída"
2. Clica no campo de data
3. Seleciona amanhã (04/11/2025)
4. Escolhe a hora (ex: 09:00)
5. Preenche outros dados
6. Clica em "Registrar"
7. Viagem aparece em "Cronograma" para amanhã
8. Quando chegar o horário, motorista segue o trajeto
```

### Cenário 3: Cancelar Viagem Agendada
```
1. Admin visualiza o cronograma
2. Vê uma viagem agendada
3. Por algum motivo, precisa cancelá-la
4. Clica no botão "Cancelar"
5. Confirma no modal
6. Viagem muda para "Cancelada"
7. Veículo volta a "Disponível"
```

---

## 📋 Estrutura da Planilha Atualizada

### DB_Viagens
```
[1]  ID
[2]  Motorista
[3]  PlacaVeiculo
[4]  KmInicial
[5]  KmFinal
[6]  DataSaida          ← Agora permite qualquer data
[7]  HoraSaida          ← Agora permite qualquer hora
[8]  DataChegada
[9]  HoraChegada
[10] Destinos
[11] Status             ← Pode ser: "Em Rota", "Finalizada", "Cancelada"
[12] Passageiros
[13] Observacoes
```

---

## 🔒 Permissões por Papel

| Ação | Motorista | Admin |
|------|-----------|-------|
| Registrar Saída | ✅ Própria | ✅ Qualquer |
| Visualizar Cronograma | ✅ | ✅ |
| Registrar Chegada | ✅ | ✅ |
| Cancelar Viagem | ❌ | ✅ |
| Ver Histórico | ✅ | ✅ |

---

## 🐛 Troubleshooting

### "Data não está sendo preenchida"
- Limpe o cache (Ctrl+Shift+Del)
- Recarregue a página

### "Botão de cancelamento não aparece"
- Verifique se você está logado como **admin**
- Apenas admins podem cancelar viagens

### "Viagem desapareceu mas continua no histórico"
- Isso é normal!
- Viagens canceladas saem do cronograma mas permanecem no histórico com status "Cancelada"

---

## 📊 Casos de Uso Recomendados

### 1. Manutenção Preventiva
```
Admin agenda saída para manutenção:
- Data: 10/11/2025
- Hora: 08:00
- Destino: "Oficina - Manutenção"
- Observação: "Revisão completa do motor"
```

### 2. Emergência / Cancelamento
```
Admin precisa cancelar saída:
- Clica no botão "Cancelar" no cronograma
- Viagem é cancelada imediatamente
- Veículo volta a disponível
```

### 3. Agendamento de Rota Fixa
```
Admin agenda saída recorrente:
- Toda segunda-feira às 09:00
- Mesma rota (centros, filiais)
- Registra como viagem agendada
```

---

## 🎯 Próximas Melhorias Possíveis

1. ✨ **Viagens Recorrentes**: Agendar mesma rota para vários dias
2. ✨ **Lembretes**: Notificação quando viagem está próxima
3. ✨ **Relatório de Canceladas**: Dashboard com motivos de cancelamento
4. ✨ **Re-agendar**: Opção de reagendar ao invés de cancelar
5. ✨ **Histórico de Alterações**: Log de quem cancelou e quando

---

## 📝 Resumo das Mudanças

| Item | Antes | Depois |
|------|-------|--------|
| Data de Saída | Preenchida automaticamente | Escolhida pelo usuário |
| Hora de Saída | Preenchida automaticamente | Escolhida pelo usuário |
| Cancelamento | Não era possível | Apenas admin pode |
| Status de Viagem | "Em Rota" ou "Finalizada" | Agora inclui "Cancelada" |

---

**Data**: 03/11/2025  
**Versão**: 1.1  
**Status**: ✅ Implementado e Testado
