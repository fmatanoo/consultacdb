# Sistema de Consulta Customer ID

Sistema simples para carregar planilhas CSV e consultar o status de customer_ids.

## 🚀 Funcionalidades

- ✅ **Upload simples** de planilhas CSV
- ✅ **Consulta rápida** por customer_id
- ✅ **Histórico completo** de todas as planilhas
- ✅ **Status atual** (ativo/inativo)
- ✅ **Relatórios** em CSV
- ✅ **Interface responsiva** para mobile
- ✅ **Duas interfaces separadas** (admin e consulta)

## 📋 Pré-requisitos

- Python 3.7 ou superior
- Git (para clonar o repositório)

## 🛠️ Instalação

### 1. Clonar o repositório
```bash
git clone https://github.com/SEU_USUARIO/consulta_excel.git
cd consulta_excel
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Executar o sistema
```bash
python app.py
```

### 4. Acessar no navegador
```
http://localhost:5000
```

## 🔗 URLs do Sistema

- **Consulta Pública**: `http://localhost:5000/` (para atendimento)
- **Área Administrativa**: `http://localhost:5000/admin` (para você)

## 📊 Como Usar

### Interface Administrativa (`/admin`)
**Para carregar planilhas:**

1. Acesse: `http://localhost:5000/admin`
2. Clique em "Carregar Nova Planilha"
3. Selecione um arquivo CSV com a coluna `customer_id`
4. Clique em "Carregar Planilha"

### Interface de Consulta (`/`)
**Para atendimento ao cliente:**

1. Acesse: `http://localhost:5000`
2. Digite o customer_id no campo de busca
3. Clique em "Consultar"
4. Veja o resultado:
   - ✅ **Ativo**: Customer está na última planilha
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

## 🚀 Deploy

### Vercel (Recomendado)
1. Faça fork deste repositório
2. Conecte ao Vercel
3. Configure as variáveis de ambiente se necessário
4. Deploy automático!

### Outros provedores
O sistema funciona em qualquer provedor que suporte Python/Flask.

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

## 🛠️ Tecnologias

- **Backend**: Flask, SQLAlchemy, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Processamento**: Pandas
- **Deploy**: Vercel

## 📞 Suporte

Se precisar de ajuda:
- Verifique se o CSV tem a coluna `customer_id`
- Confirme que o arquivo é válido
- Teste com o arquivo de exemplo fornecido

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido para facilitar a consulta de customer_ids de forma simples e intuitiva!** 🎉 