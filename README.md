# Sistema de Consulta Customer ID

Sistema web para consulta de customer IDs com histórico completo de planilhas CSV carregadas e banco PostgreSQL.

## 🚀 Funcionalidades

### **Interface de Consulta (Pública)**
- Busca por customer_id
- Mostra status atual (ativo/inativo)
- Exibe histórico completo de participação
- Interface simples para atendimento

### **Interface Administrativa**
- Upload de planilhas CSV
- Visualização de estatísticas
- Histórico de todas as planilhas carregadas
- Geração de relatórios CSV
- Controle de acesso restrito

### **Rastreamento de Histórico**
- **Data de entrada**: Quando o customer_id apareceu pela primeira vez
- **Data de saída**: Quando o customer_id saiu da lista (se aplicável)
- **Status atual**: Se está ativo na última planilha
- **Histórico completo**: Todas as planilhas onde participou

## 📊 Banco de Dados PostgreSQL

### **Tabelas:**
- **Planilha**: Registro de cada upload
- **Customer**: Histórico completo de cada customer_id

### **Rastreamento Automático:**
```
Planilha 1: [123, 456, 789] → Todos ativos
Planilha 2: [123, 456] → 789 fica inativo
Planilha 3: [123, 999] → 456 fica inativo, 999 novo ativo
```

## 🛠️ Tecnologias

- **Backend**: Flask + SQLAlchemy
- **Banco**: PostgreSQL (Render)
- **Frontend**: HTML + CSS + JavaScript
- **Deploy**: Render.com

## 📁 Estrutura do Projeto

```
consulta_excel/
├── app.py                    # Aplicação principal
├── requirements.txt          # Dependências Python
├── render.yaml              # Configuração Render
├── templates/
│   ├── consulta.html       # Interface de consulta
│   └── admin.html          # Interface administrativa
├── static/
│   ├── styles.css          # Estilos CSS
│   ├── admin.js            # JavaScript admin
│   └── consulta.js         # JavaScript consulta
├── exemplo_customers.csv   # Arquivo de exemplo
├── CONFIGURAR_BANCO_RENDER.md # Guia de configuração
├── README.md               # Documentação
├── LICENSE                 # Licença MIT
└── .gitignore             # Arquivos ignorados
```

## 🚀 Deploy no Render

### **Passos Rápidos:**

1. **Criar conta no Render**: https://render.com
2. **Criar banco PostgreSQL**:
   - New → PostgreSQL
   - Name: `consulta-excel-db`
   - Plan: Free
3. **Criar Web Service**:
   - New → Web Service
   - Conectar repositório GitHub
   - Build: `pip install -r requirements.txt`
   - Start: `python app.py`
4. **Configurar DATABASE_URL**:
   - Environment → DATABASE_URL (copiar do banco)
5. **Deploy**: Create Web Service

### **Configuração Detalhada:**
Veja `CONFIGURAR_BANCO_RENDER.md` para instruções completas.

## 📋 Formato do CSV

### **Estrutura:**
```csv
customer_id
12345
67890
11111
```

### **Requisitos:**
- Arquivo CSV
- Coluna obrigatória: `customer_id`
- Sem outras colunas necessárias
- Encoding: UTF-8

## 🔍 Como Usar

### **Para Administradores:**
1. Acesse `/admin`
2. Faça upload de planilhas CSV
3. Monitore estatísticas
4. Gere relatórios

### **Para Atendimento:**
1. Acesse `/` (página principal)
2. Digite o customer_id
3. Veja status e histórico

## 📈 Relatórios

### **Relatório CSV inclui:**
- Customer ID
- Data de entrada
- Data de saída
- Status atual
- Total de planilhas

## 🔧 Desenvolvimento Local

### **Instalar dependências:**
```bash
pip install -r requirements.txt
```

### **Executar localmente:**
```bash
python app.py
```

### **Acessar:**
- **Local**: http://localhost:5000
- **Admin**: http://localhost:5000/admin

## 📝 Licença

MIT License - veja arquivo LICENSE.

---

**Sistema completo com histórico persistente e rastreamento automático!** 🎉 