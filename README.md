# Sistema de Consulta Customer ID

Sistema simples para carregar planilhas CSV e consultar o status de customer_ids.

## 🚀 Como Usar

### 📊 **Interface Administrativa** (`/admin`)
**Acesso restrito para você carregar planilhas:**

1. **Carregar Planilha CSV**
   - Acesse: `http://localhost:5000/admin`
   - Clique em "Carregar Nova Planilha"
   - Selecione um arquivo CSV que contenha a coluna `customer_id`
   - Clique em "Carregar Planilha"
   - O sistema processará automaticamente

2. **Ver Histórico**
   - Visualize todas as planilhas carregadas
   - Veja quantos customers estão ativos em cada planilha
   - Acompanhe as datas de upload

3. **Baixar Relatório**
   - Clique em "Baixar Relatório CSV"
   - Receba um arquivo com todos os customers e seus status

### 🔍 **Interface de Consulta** (`/`)
**Acesso público para atendimento:**

1. **Consultar Customer ID**
   - Acesse: `http://localhost:5000`
   - Digite o customer_id no campo de busca
   - Clique em "Consultar" ou pressione Enter
   - Veja o resultado:
     - ✅ **Ativo**: Customer está na última planilha carregada
     - ⚠️ **Inativo**: Customer participou antes, mas não está mais ativo
     - ❌ **Não encontrado**: Customer nunca esteve nas planilhas

## 📋 Formato do CSV

Seu arquivo CSV deve ter apenas uma coluna:

```csv
customer_id
12345
67890
11111
```

## 🛠️ Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

2. **Executar o sistema:**
```bash
python app.py
```

3. **Acessar no navegador:**
```
http://localhost:5000
```

## 📊 Funcionalidades

- ✅ **Upload simples** de planilhas CSV
- ✅ **Consulta rápida** por customer_id
- ✅ **Histórico completo** de todas as planilhas
- ✅ **Status atual** (ativo/inativo)
- ✅ **Relatórios** em CSV
- ✅ **Interface responsiva** para mobile

## 🔧 Deploy no Vercel

Para colocar online no Vercel:

1. **Criar arquivo `vercel.json`:**
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

2. **Fazer upload no Vercel**
3. **Configurar variáveis de ambiente se necessário**

## 📁 Estrutura do Projeto

```
consulta_excel/
├── app.py                 # Aplicação principal
├── templates/
│   ├── consulta.html     # Interface de consulta pública
│   └── admin.html        # Interface administrativa
├── static/
│   ├── styles.css        # Estilos
│   ├── consulta.js       # JavaScript da consulta
│   └── admin.js          # JavaScript do admin
├── uploads/              # Pasta para arquivos carregados
├── customer_tracking.db  # Banco de dados SQLite
├── requirements.txt      # Dependências Python
└── exemplo_customers.csv # Arquivo de exemplo
```

## 🔗 URLs do Sistema

- **Consulta Pública**: `http://localhost:5000/` (para atendimento)
- **Área Administrativa**: `http://localhost:5000/admin` (para você)

## 🎯 Exemplo de Uso

1. **Carregue a primeira planilha** com customers ativos
2. **Carregue uma segunda planilha** (alguns customers podem sair)
3. **Consulte um customer_id** para ver se está ativo
4. **Veja o histórico** de quando entrou e saiu

## 📞 Suporte

Se precisar de ajuda:
- Verifique se o CSV tem a coluna `customer_id`
- Confirme que o arquivo é válido
- Teste com o arquivo de exemplo fornecido

---

**Desenvolvido para facilitar a consulta de customer_ids de forma simples e intuitiva!** 🎉 