# Configuração do Render

## 🎯 **Configuração do Banco PostgreSQL:**

### **1. Verificar o banco existente**
1. Vá para https://dashboard.render.com
2. Clique em "Databases"
3. Encontre seu banco `consulta-excel-db`
4. Clique nele

### **2. Copiar a DATABASE_URL**
1. No seu banco, vá em "Connections"
2. Copie a "External Database URL"
3. Exemplo: `postgres://user:pass@host:port/database`

### **3. Configurar no Web Service**
1. Vá para seu Web Service
2. Clique em "Environment"
3. Adicione variável:
   - **Key**: `DATABASE_URL`
   - **Value**: Cole a URL do banco
4. Clique "Save Changes"

### **4. Deploy**
1. Vá em "Manual Deploy"
2. Clique "Deploy latest commit"
3. Aguarde o build

## 🔧 **Verificação da Configuração**

### **Logs de Build**
Durante o deploy, verifique se aparece:
```
✅ Installing Flask-SQLAlchemy==3.0.5
✅ Installing psycopg2-binary==2.9.7
✅ Installing SQLAlchemy==2.0.21
```

### **Logs de Runtime**
Após o deploy, verifique se aparece:
```
✅ DATABASE_URL encontrada!
✅ Tabelas criadas com sucesso!
```

## 🚨 **Possíveis Problemas e Soluções**

### **Problema 1: "ModuleNotFoundError: flask_sqlalchemy"**
**Solução**: O build command está correto no `render.yaml`

### **Problema 2: "DATABASE_URL not found"**
**Solução**: Verificar se a variável está configurada no Environment

### **Problema 3: "Connection refused"**
**Solução**: Verificar se o banco está ativo no Render

## 🧪 **Teste Local (Opcional)**

Se quiser testar localmente:

```bash
# Instalar dependências
pip install Flask Flask-SQLAlchemy psycopg2-binary

# Configurar DATABASE_URL
export DATABASE_URL="sua_url_do_banco"

# Testar conexão
python test_db.py
```

## 📊 **Estrutura do Banco**

Após o deploy bem-sucedido, o sistema criará:

### **Tabela: planilha**
- `id` (Primary Key)
- `nome_arquivo` (String)
- `data_upload` (DateTime)
- `quantidade_registros` (Integer)
- `data_planilha` (Date)
- `created_at` (DateTime)

### **Tabela: customer**
- `id` (Primary Key)
- `customer_id` (String)
- `planilha_id` (Foreign Key)
- `data_entrada` (Date)
- `data_saida` (Date, nullable)
- `ativo` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## 🎉 **Resultado Esperado**

Após configuração correta:
- ✅ Sistema conecta ao PostgreSQL
- ✅ Tabelas são criadas automaticamente
- ✅ Upload de planilhas funciona
- ✅ Consultas retornam dados do banco
- ✅ Histórico é preservado

---

**Com o banco já configurado, é só conectar e usar!** 🚀 