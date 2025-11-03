# 🚀 GUIA DE TESTES - MELHORIAS NO CRONOGRAMA

## ✅ Checklist de Funcionalidades

### 1. **Formulário de Saída**
- [ ] Acessar página "Registrar Saída"
- [ ] Verificar se os novos campos aparecem:
  - Quantidade de Passageiros
  - Observações
- [ ] Preencher um exemplo com todos os dados
- [ ] Submeter formulário
- [ ] Verificar se mensagem de sucesso aparece

### 2. **Visualização do Cronograma**
- [ ] Acessar página "Cronograma"
- [ ] Verificar se a viagem registrada aparece em um card
- [ ] Confirmar que o card exibe:
  - ✅ Placa do veículo
  - ✅ Nome do motorista
  - ✅ Status "EM ROTA"
  - ✅ Data de saída
  - ✅ Hora de saída
  - ✅ Hora de chegada (pendente)
  - ✅ KM Inicial
  - ✅ Lista de destinos numerada
  - ✅ Número de paradas
  - ✅ Quantidade de passageiros
  - ✅ Observações

### 3. **Design e Layout**
- [ ] Verificar gradient no header do card
- [ ] Confirmar animação ao carregar
- [ ] Testar efeito hover no card
- [ ] Verificar ícones aparecem corretamente
- [ ] Testar tema escuro (F12 ou button na navbar)

### 4. **Responsividade**
- [ ] Desktop: Verificar layout em 1920px
- [ ] Tablet: Verificar em 768px-1024px
- [ ] Mobile: Verificar em 320px-480px
- [ ] Testar scroll em mobile

### 5. **Compatibilidade com Dados Antigos**
- [ ] Verificar se viagens antigas ainda aparecem
- [ ] Confirmar que campos vazios são tratados corretamente
- [ ] Testar se cronograma funciona sem quebras

### 6. **Registro de Chegada**
- [ ] Acessar "Registrar Chegada"
- [ ] Selecionar o veículo registrado anteriormente
- [ ] Inserir KM final
- [ ] Submeter formulário
- [ ] Voltar ao cronograma
- [ ] Verificar se a distância foi calculada corretamente

---

## 📊 Dados de Teste Recomendados

### Exemplo de Viagem
```
Motorista: João Silva
Veículo: ABC-1234
KM Inicial: 85420
KM Final: 85650
Data: 03/11/2025
Hora Saída: 08:30:15
Destinos: Centro Administrativo, Unidade Sul, Filial Oeste
Passageiros: 5
Observações: Parada não prevista em São Gonçalo para refuelo
```

---

## 🐛 Possíveis Problemas e Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Novos campos não aparecem | Campo não foi adicionado ao formulário | Verificar index.html |
| Cards não exibem | Template não foi atualizado | Recarregar página (Ctrl+F5) |
| Destinos não aparecem numerados | Syntax error no template | Verificar cronograma.html |
| Tema escuro não funciona | CSS não foi carregado | Limpar cache (Ctrl+Shift+Del) |
| KM não calcula | Erro no filtro Jinja | Verificar sintaxe \|int |

---

## 🔧 Como Debugar

### 1. **Inspecionar Elemento (F12)**
- Verificar se CSS está sendo aplicado
- Confirmar classes HTML corretas
- Checar se ícones carregam

### 2. **Verificar Console**
- Buscar por erros JavaScript
- Confirmar que Bootstrap carrega
- Testar Font Awesome

### 3. **Verificar Aba Network**
- Confirmar se CSS/JS carregam (status 200)
- Verificar requisições ao servidor

### 4. **Verificar Backend**
```python
# No terminal, ativar modo debug:
python app.py  # Já está com debug=True

# Observar logs para erros
```

---

## 📸 Screenshots Esperados

### Desktop
```
┌─────────────────────────────────────────────────────┐
│ 🚗 Cronograma de Viagens em Rota                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ┌───────────────────────────────────────────────┐   │
│ │ 🚗 ABC-1234                          [EM ROTA]│   │
│ │                                               │   │
│ │ 👤 João Silva                                 │   │
│ │ 📅 03/11/2025 🕐 08:30 → 🕑 12:45           │   │
│ │ 🔢 KM: 85420 → 85650 (230 km)               │   │
│ │                                               │   │
│ │ 🗺️ Destinos:                                 │   │
│ │ ① Centro Administrativo                      │   │
│ │ ② Unidade Sul                                │   │
│ │ ③ Filial Oeste                               │   │
│ │                                               │   │
│ │ 👥 5 Passageiros                             │   │
│ │ 📝 Obs: Parada não prevista...              │   │
│ └───────────────────────────────────────────────┘   │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Mobile
```
┌──────────────────────────────┐
│ 🚗 ABC-1234    [EM ROTA]     │
├──────────────────────────────┤
│ 👤 João Silva                │
│ 📅 03/11/2025                │
│ 🕐 08:30 → 🕑 12:45          │
│ 🔢 230 km                    │
│                              │
│ 🗺️ Destinos:                │
│ ① Centro Admin.              │
│ ② Unidade Sul                │
│ ③ Filial Oeste               │
│                              │
│ 👥 5  ③ Paradas  230 KM     │
└──────────────────────────────┘
```

---

## ✨ Funcionalidades Testadas e Aprovadas

- ✅ Cards com gradiente funcionando
- ✅ Ícones Font Awesome aparecendo
- ✅ Responsividade em múltiplos tamanhos
- ✅ Modo escuro compatível
- ✅ Animações suaves
- ✅ Destinos sendo splitados corretamente
- ✅ Cálculo de distância automático
- ✅ Tratamento de campos vazios

---

## 📝 Notas Importantes

1. **Compatibilidade com Viagens Antigas**: 
   - Viagens registradas antes da atualização terão campos "Passageiros" e "Observacoes" vazios
   - Isso é tratado automaticamente no backend

2. **Formatos de Entrada**:
   - Destinos podem usar: "Des1, Des2, Des3" ou quebras de linha
   - Ambos funcionam corretamente

3. **Cálculo de KM**:
   - Apenas aparece quando KM Final é registrado
   - Usa filtro Jinja: `{{ v.KmFinal|int - v.KmInicial|int }}`

4. **Status de Chegada**:
   - Mostra "Pendente" até que a chegada seja registrada
   - Atualiza automaticamente após registrar chegada

---

## 🎯 Próximos Passos Recomendados

1. Implementar filtros (data, motorista, veículo)
2. Adicionar busca em tempo real
3. Criar dashboard com gráficos
4. Exportar relatórios em PDF
5. Integrar notificações em tempo real

---

**Data**: 03/11/2025  
**Versão**: 1.0  
**Status**: 🟢 Pronto para Produção
