# Configuração do Render com PostgreSQL

## 🚀 Passos para Deploy

### 1. **Criar conta no Render**
- Vá para: https://render.com
- Faça login com GitHub

### 2. **Criar Banco de Dados PostgreSQL**
1. Clique em "New +"
2. Escolha "PostgreSQL"
3. Configure:
   - **Name**: `consulta-excel-db`
   - **Database**: `consulta_excel`
   - **User**: `consulta_user`
   - **Plan**: Free
4. Clique em "Create Database"

### 3. **Criar Web Service**
1. Clique em "New +"
2. Escolha "Web Service"
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `consulta-excel`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free

### 4. **Configurar Variáveis de Ambiente**
No seu Web Service, vá em "Environment":
- **DATABASE_URL**: Copie a URL do banco PostgreSQL criado

### 5. **Deploy**
- Clique em "Create Web Service"
- Aguarde o deploy (2-3 minutos)

## 📊 Funcionalidades do Banco

### **Tabela Planilha**
- `id`: ID único da planilha
- `nome_arquivo`: Nome do arquivo CSV
- `data_upload`: Data/hora do upload
- `quantidade_registros`: Total de registros
- `data_planilha`: Data da planilha
- `created_at`: Data de criação

### **Tabela Customer**
- `id`: ID único do registro
- `customer_id`: ID do customer
- `planilha_id`: Referência à planilha
- `data_entrada`: Data de entrada
- `data_saida`: Data de saída (null se ativo)
- `ativo`: Status atual (true/false)
- `created_at`: Data de criação
- `updated_at`: Data de atualização

## 🔍 Rastreamento de Histórico

### **Como funciona:**
1. **Primeira planilha**: Todos os customers ficam ativos
2. **Planilhas seguintes**: 
   - Customers que saíram ficam inativos
   - Customers que entraram ficam ativos
   - Histórico completo preservado

### **Exemplo:**
```
Planilha 1: [123, 456, 789] - Todos ativos
Planilha 2: [123, 456] - 789 fica inativo, 123 e 456 continuam ativos
Planilha 3: [123, 999] - 456 fica inativo, 123 continua ativo, 999 novo ativo
```

## 📈 Relatórios

### **Relatório CSV inclui:**
- Customer ID
- Data de entrada
- Data de saída
- Status atual
- Total de planilhas onde apareceu

## 🔧 Manutenção

### **Backup do banco:**
- Render faz backup automático
- Pode exportar dados via interface

### **Monitoramento:**
- Logs disponíveis no Render
- Métricas de performance
- Alertas automáticos

## 🎯 URLs Finais

- **Site**: `https://seu-app.onrender.com`
- **Admin**: `https://seu-app.onrender.com/admin`
- **Consulta**: `https://seu-app.onrender.com`

---

**Agora você tem um sistema completo com histórico persistente!** 🎉 