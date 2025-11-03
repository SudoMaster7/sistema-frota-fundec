# 🎨 Guia de Customização Visual

Docum ento com instruções para customizar cores, fontes e outros elementos visuais do sistema.

---

## 🌈 Alterando Cores Principais

### Método 1: Via CSS Variables (Recomendado)

Edite o arquivo `static/css/style.css` no bloco `:root`:

```css
:root {
    --bs-primary: #667eea;        /* Roxo principal - ALTERE AQUI */
    --bs-primary-rgb: 102, 126, 234;  /* RGB da cor principal */
    --bs-link-color: #667eea;     /* Cor de links */
    --bs-link-hover-color: #764ba2;   /* Roxo escuro - secundária */
    --color-success: #10b981;     /* Verde */
    --color-warning: #f59e0b;     /* Amarelo */
    --color-danger: #ef4444;      /* Vermelho */
    --color-info: #3b82f6;        /* Azul */
}
```

### Exemplos de Temas:

#### Tema Azul:
```css
--bs-primary: #3b82f6;           /* Azul principal */
--bs-primary-rgb: 59, 130, 246;
--bs-link-hover-color: #1e40af;  /* Azul escuro */
```

#### Tema Verde:
```css
--bs-primary: #10b981;           /* Verde principal */
--bs-primary-rgb: 16, 185, 129;
--bs-link-hover-color: #059669;  /* Verde escuro */
```

#### Tema Laranja:
```css
--bs-primary: #f97316;           /* Laranja principal */
--bs-primary-rgb: 249, 115, 22;
--bs-link-hover-color: #c2410c;  /* Laranja escuro */
```

### Método 2: Via Gradientes Personalizados

Procure por gradientes em `style.css` e `templates/*.html`:

**Atual:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**Novo (Exemplo - Azul para Ciano):**
```css
background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
```

---

## 🔤 Alterando Fontes

### Alterar Font Family Global:

Em `static/css/style.css`:

```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
```

Opções populares:
- `'Inter', sans-serif` (moderna)
- `'Poppins', sans-serif` (futurista)
- `'Open Sans', sans-serif` (profissional)
- `'Roboto', sans-serif` (limpa)

**Para usar Google Fonts, adicione em `base.html`:**

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
```

Depois use no CSS:
```css
body {
    font-family: 'Poppins', sans-serif;
}
```

---

## 📏 Alterando Tamanhos

### Tamanhos de Fonte Global:

```css
body {
    font-size: 16px;  /* Altere para maior/menor */
}

h1 {
    font-size: 2rem;  /* Headers */
}

h2 {
    font-size: 1.5rem;
}

p {
    font-size: 1rem;  /* Parágrafo */
}
```

### Padding e Margin:

```css
/* Em cards */
.card-body {
    padding: 2rem;  /* Altere para 1rem ou 3rem */
}

/* Em content sections */
.content-section {
    padding: 2rem;  /* Altere para maior/menor */
}
```

---

## 🎭 Dark Mode Customizado

### Alterar cores do Dark Mode:

Em `static/css/style.css`, procure por `[data-bs-theme="dark"]`:

```css
[data-bs-theme="dark"] {
    --bs-body-bg: #1a202c;    /* Background muito escuro */
    --bs-body-color: #f7fafc; /* Texto branco */
}

[data-bs-theme="dark"] .card {
    background-color: #2d3748;  /* Cards em dark mode */
}

[data-bs-theme="dark"] .form-control {
    background-color: #3d4556;  /* Inputs em dark mode */
}
```

Opções de cores escuras:
- Muito escuro: `#0f172a` ou `#1a202c`
- Escuro médio: `#1e293b` ou `#2d3748`
- Cinza escuro: `#334155` ou `#3d4556`

---

## 🔘 Alterando Buttons

### Cores de Botões:

Em `static/css/style.css`:

```css
.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.btn-primary:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);  /* Invertido */
}
```

### Tamanho de Botões:

```css
.btn-lg {
    padding: 1rem;      /* Altere para maior/menor */
    font-size: 1rem;
}

.btn-sm {
    padding: 0.4rem;
    font-size: 0.85rem;
}
```

### Borda Arredondada:

```css
.btn {
    border-radius: 8px;  /* Altere para 0px (reto), 50px (bem arredondado) */
}
```

---

## 📦 Alterando Cards

### Estilos de Card:

```css
.card {
    border-radius: 12px;  /* Arredondamento - altere para 0, 8, 20 */
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);  /* Sombra */
    border: none;
}

.card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);  /* Sombra ao hover */
}
```

Alterar para cards com borda:
```css
.card {
    border: 2px solid #e5e7eb;  /* Adicione borda */
}
```

---

## 🎯 Alterando Grid Responsivo

### Stats Grid (4 cards):

Procure em `style.css`:
```css
.stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
}
```

Opções:
- Mais estreito: `minmax(150px, 1fr)`
- Mais largo: `minmax(300px, 1fr)`
- Colunas fixas: `repeat(4, 1fr)` (sempre 4 colunas)

### Quick Actions Grid:

```css
.quick-actions {
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}
```

---

## 📱 Customizar Breakpoints

Em `static/css/style.css`:

```css
/* Tablet */
@media (max-width: 768px) {
    .dashboard-header h1 {
        font-size: 1.5rem;  /* Altere para maior/menor */
    }
}

/* Mobile grande */
@media (max-width: 480px) {
    .quick-action-btn {
        padding: 0.8rem;  /* Altere */
    }
}
```

---

## 🎪 Adicionar Padrões de Fundo

### Em elementos específicos:

```css
.dashboard-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;  /* Fundo fixo ao scroll */
}
```

### Padrão de pontos (usando CSS):

```css
.dashboard-header {
    background-image: 
        radial-gradient(circle, rgba(255,255,255,.1) 1px, transparent 1px);
    background-size: 20px 20px;
}
```

---

## 🌟 Adicionar Animações Personalizadas

Em `static/css/style.css`:

```css
/* Animação de pulso */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.5;
    }
}

.stat-value {
    animation: pulse 2s infinite;  /* Aplica animação */
}

/* Animação de deslize */
@keyframes slideInRight {
    from {
        transform: translateX(100px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.quick-action-btn {
    animation: slideInRight 0.5s ease;
}
```

---

## 🎨 Exemplos Completos de Temas

### Tema 1: Tech Dark (Azul/Ciano)

```css
:root {
    --bs-primary: #06b6d4;           /* Ciano */
    --bs-link-hover-color: #0891b2;  /* Ciano escuro */
    --color-success: #06b6d4;
}

.dashboard-header {
    background: linear-gradient(135deg, #0f766e 0%, #06b6d4 100%);
}

.btn-primary {
    background: linear-gradient(135deg, #0891b2 0%, #06b6d4 100%);
}
```

### Tema 2: Nature (Verde/Terra)

```css
:root {
    --bs-primary: #22c55e;           /* Verde */
    --bs-link-hover-color: #16a34a;  /* Verde escuro */
    --color-success: #16a34a;
}

.dashboard-header {
    background: linear-gradient(135deg, #22c55e 0%, #15803d 100%);
}
```

### Tema 3: Elegant (Ouro/Roxo)

```css
:root {
    --bs-primary: #d97706;           /* Ouro */
    --bs-link-hover-color: #92400e;  /* Ouro escuro */
    --color-success: #d97706;
}

.dashboard-header {
    background: linear-gradient(135deg, #d97706 0%, #6d28d9 100%);
}
```

---

## 📝 Checklist de Customização

- [ ] Cores principais alteradas
- [ ] Cores de gradiente atualizadas
- [ ] Font alterada (se desejado)
- [ ] Tamanhos de fonte ajustados
- [ ] Padding/Margin personalizados
- [ ] Dark mode testado
- [ ] Botões customizados
- [ ] Grid responsivo testado
- [ ] Mobile testado
- [ ] Dark mode testado com novo tema

---

## 🚨 Cuidados ao Customizar

1. **Sempre fazer backup** do arquivo original antes de editar
2. **Testar em múltiplos navegadores** (Chrome, Firefox, Safari, Edge)
3. **Verificar responsividade** em celular após mudanças
4. **Testar dark mode** se alterou cores
5. **Validar contraste** das cores (legibilidade)
6. **Usar Dev Tools** (F12) para preview de mudanças

---

## 🔍 Ferramentas Úteis

### Gerador de Gradientes:
- https://cssgradient.io/

### Paleta de Cores:
- https://coolors.co/

### Verificar Contraste:
- https://webaim.org/resources/contrastchecker/

### Fonte Customizada:
- https://fonts.google.com/

---

## ❓ Dúvidas Comuns

### P: Como reverter para o tema original?
**R:** Se não fez backup, copie os valores do arquivo de versão anterior ou git history.

### P: As mudanças não aparecem?
**R:** Pressione `Ctrl+Shift+R` para limpar cache do navegador.

### P: Como adicionar logo personalizada?
**R:** Edite `templates/base.html` e altere o `navbar-brand`.

### P: Posso usar imagem de background?
**R:** Sim! Use: `background-image: url('/static/img/background.jpg');`

---

**Boa customização!** 🎉
