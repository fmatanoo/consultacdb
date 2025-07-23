# Guia do Sistema de Importação CSV e Rastreamento de Elegibilidade

## 📋 Visão Geral

O sistema foi completamente reformulado para trabalhar com **importação de arquivos CSV** e **rastreamento de elegibilidade** dos usuários. Agora você pode:

- **Importar arquivos CSV** com dados dos usuários
- **Manter histórico completo** de todas as importações
- **Rastrear elegibilidade** de cada customer_id ao longo do tempo
- **Verificar se um usuário já esteve elegível** em alguma das atualizações
- **Visualizar estatísticas** em tempo real

## 🚀 Como Executar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Iniciar a Aplicação

```bash
python app.py
```

A aplicação será iniciada em `http://localhost:5000`

### 3. Acessar a Interface

Abra seu navegador e acesse:
```
http://localhost:5000
```

## 📊 Funcionalidades Principais

### 1. Importação de CSV

#### Estrutura do Arquivo CSV
O arquivo CSV deve conter as seguintes colunas:

```csv
customer_id,nome,email,telefone
25499984,João Silva,joao.silva@email.com,(11) 99999-1111
26069015,Maria Santos,maria.santos@email.com,(11) 99999-2222
```

#### Colunas Obrigatórias
- **customer_id**: Identificador único do usuário (obrigatório)
- **nome**: Nome do usuário (opcional)
- **email**: Email do usuário (opcional)
- **telefone**: Telefone do usuário (opcional)

#### Processo de Importação
1. **Selecionar arquivo CSV** na interface
2. **Clicar em "Importar"**
3. **Sistema processa automaticamente**:
   - Valida o arquivo
   - Verifica se customer_id já existe
   - Cria novos usuários ou atualiza existentes
   - Registra elegibilidade na importação atual
   - Salva histórico completo

### 2. Busca e Rastreamento

#### Buscar Usuário
- Digite o **customer_id** no campo de busca
- Sistema retorna:
  - **Dados do usuário** (nome, email, telefone)
  - **Status atual** de elegibilidade
  - **Histórico completo** de todas as importações
  - **Timeline** de quando esteve elegível

#### Informações Retornadas
- ✅ **Dados pessoais** do usuário
- ✅ **Data de cadastro** e última atualização
- ✅ **Status atual** (elegível/não elegível)
- ✅ **Histórico completo** de importações
- ✅ **Timeline** de elegibilidade

### 3. Histórico de Importações

#### Visualização
- **Lista de todas as importações** realizadas
- **Data e hora** de cada importação
- **Quantidade de registros** processados
- **Status** da importação (concluído/processando)
- **Observações** detalhadas

#### Detalhes por Importação
- Nome do arquivo importado
- Data e hora da importação
- Quantidade de registros processados
- Novos usuários vs atualizações
- Status de conclusão

### 4. Lista de Usuários

#### Visualização
- **Cards informativos** para cada usuário
- **Dados principais** (customer_id, nome, email)
- **Status de elegibilidade** atual
- **Data de cadastro**

#### Paginação
- Sistema carrega **12 usuários por vez**
- **Navegação automática** conforme necessário
- **Performance otimizada** para grandes volumes

## 🗄️ Estrutura do Banco de Dados

### Tabelas Criadas

#### 1. Importacao
```sql
- id (Primary Key)
- nome_arquivo (String)
- data_importacao (DateTime)
- quantidade_registros (Integer)
- status (String)
- observacoes (Text)
```

#### 2. Usuario
```sql
- id (Primary Key)
- customer_id (String, Unique)
- nome (String)
- email (String)
- telefone (String)
- data_cadastro (DateTime)
- ultima_atualizacao (DateTime)
```

#### 3. HistoricoElegibilidade
```sql
- id (Primary Key)
- customer_id (String)
- importacao_id (Foreign Key)
- data_importacao (DateTime)
- elegivel (Boolean)
- observacoes (Text)
```

## 📈 Estatísticas em Tempo Real

### Header da Aplicação
- **Total de usuários** cadastrados
- **Total de importações** realizadas
- **Importações hoje** (data atual)

### Atualizações Automáticas
- Estatísticas atualizadas **após cada importação**
- **Contadores em tempo real**
- **Histórico preservado** permanentemente

## 🔍 Rastreamento de Elegibilidade

### Como Funciona
1. **Cada importação** registra a elegibilidade de todos os usuários
2. **Histórico completo** é mantido para cada customer_id
3. **Timeline visual** mostra quando o usuário esteve elegível
4. **Status atual** é sempre a última importação

### Informações Disponíveis
- ✅ **Primeira vez** que o usuário foi elegível
- ✅ **Última vez** que foi elegível
- ✅ **Total de vezes** que esteve elegível
- ✅ **Períodos** de elegibilidade
- ✅ **Arquivos** onde apareceu

## 🎯 Casos de Uso

### 1. Primeira Importação
- Faça upload do arquivo CSV inicial
- Sistema cria todos os usuários
- Todos ficam elegíveis na primeira importação

### 2. Atualizações Subsequentes
- Faça upload de novos arquivos CSV
- Sistema compara com dados existentes
- Atualiza informações e registra nova elegibilidade

### 3. Verificação de Elegibilidade
- Digite um customer_id na busca
- Veja se já esteve elegível em alguma importação
- Analise o histórico completo

### 4. Análise de Tendências
- Visualize histórico de importações
- Identifique padrões de elegibilidade
- Monitore evolução dos dados

## 🛠️ Configuração e Personalização

### Modificar Estrutura do CSV
Para adicionar novas colunas, edite o arquivo `app.py`:

```python
# Na função importar_csv(), adicione novas colunas:
usuario.nova_coluna = row.get('nova_coluna', '')
```

### Configurar Banco de Dados
O sistema usa SQLite por padrão. Para mudar:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/dbname'
```

### Personalizar Validações
Adicione validações customizadas no arquivo `app.py`:

```python
# Exemplo: Validar formato de email
if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    # Tratar erro
```

## 📱 Interface Responsiva

### Desktop
- **Layout completo** com todas as seções
- **Grid responsivo** para cards
- **Navegação otimizada**

### Mobile
- **Layout adaptado** para telas pequenas
- **Cards empilhados** verticalmente
- **Botões otimizados** para touch

## 🔄 Atualizações e Manutenção

### Backup do Banco
```bash
# Fazer backup do banco SQLite
cp usuarios_pix.db backup_usuarios_pix.db
```

### Logs do Sistema
- **Console do navegador** para erros de frontend
- **Terminal Python** para erros de backend
- **Arquivo de log** (implementar se necessário)

### Limpeza de Dados
```sql
-- Exemplo: Limpar importações antigas
DELETE FROM HistoricoElegibilidade WHERE data_importacao < '2024-01-01';
```

## 🚨 Solução de Problemas

### Erro de Upload
- **Verificar formato** do arquivo (deve ser CSV)
- **Verificar coluna customer_id** (obrigatória)
- **Verificar permissões** da pasta uploads

### Erro de Banco de Dados
- **Verificar se o banco** foi criado corretamente
- **Verificar permissões** de escrita
- **Reiniciar aplicação** se necessário

### Performance Lenta
- **Verificar tamanho** do arquivo CSV
- **Considerar paginação** para grandes volumes
- **Otimizar consultas** se necessário

## 📞 Suporte e Contato

### Logs Importantes
- **Console do navegador** (F12)
- **Terminal Python** (onde roda a aplicação)
- **Arquivo de banco** (usuarios_pix.db)

### Próximas Melhorias
- [ ] Exportação de relatórios
- [ ] Filtros avançados
- [ ] Dashboard com gráficos
- [ ] Notificações em tempo real
- [ ] API REST completa

---

**Versão:** 3.0 - Sistema de Importação CSV e Rastreamento  
**Data:** Dezembro 2024  
**Tecnologias:** Flask, SQLAlchemy, SQLite, HTML5, CSS3, JavaScript  
**Compatibilidade:** Python 3.7+, Navegadores Modernos 