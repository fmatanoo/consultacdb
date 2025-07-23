#!/usr/bin/env python3
"""
Sistema Ultra Simples de Consulta Customer ID - Sem Banco de Dados
"""

from flask import Flask, render_template, request, jsonify
import os
import csv
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

# Armazenamento simples em memória (para demonstração)
planilhas_carregadas = []
customers_data = {}

@app.route('/')
def index():
    return render_template('consulta.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/api/upload', methods=['POST'])
def upload_csv():
    try:
        if 'arquivo' not in request.files:
            return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
        
        arquivo = request.files['arquivo']
        if arquivo.filename == '':
            return jsonify({'erro': 'Nenhum arquivo selecionado'}), 400
        
        if not arquivo.filename.endswith('.csv'):
            return jsonify({'erro': 'Apenas arquivos CSV são permitidos'}), 400
        
        # Ler CSV diretamente
        customer_ids = []
        try:
            # Decodificar o arquivo
            content = arquivo.read().decode('utf-8')
            lines = content.split('\n')
            
            # Pular cabeçalho se existir
            start_line = 0
            if lines and 'customer_id' in lines[0].lower():
                start_line = 1
            
            # Processar linhas
            for line in lines[start_line:]:
                line = line.strip()
                if line and line != 'customer_id':
                    customer_ids.append(line)
                    
        except Exception as e:
            return jsonify({'erro': f'Erro ao ler arquivo: {str(e)}'}), 400
        
        if not customer_ids:
            return jsonify({'erro': 'Nenhum customer_id válido encontrado no arquivo'}), 400
        
        # Data atual
        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # Registrar planilha
        planilha_info = {
            'id': len(planilhas_carregadas) + 1,
            'nome_arquivo': arquivo.filename,
            'data_upload': data_atual,
            'quantidade_registros': len(customer_ids),
            'customers_ativos': len(customer_ids)
        }
        planilhas_carregadas.append(planilha_info)
        
        # Atualizar customers
        for customer_id in customer_ids:
            if customer_id not in customers_data:
                customers_data[customer_id] = {
                    'ativo': True,
                    'data_entrada': data_atual,
                    'data_saida': None,
                    'planilhas': []
                }
            else:
                # Marcar como inativo na planilha anterior
                customers_data[customer_id]['ativo'] = False
                customers_data[customer_id]['data_saida'] = data_atual
                # Criar novo registro ativo
                customers_data[customer_id] = {
                    'ativo': True,
                    'data_entrada': data_atual,
                    'data_saida': None,
                    'planilhas': customers_data[customer_id]['planilhas'] + [planilha_info['nome_arquivo']]
                }
        
        return jsonify({
            'sucesso': True,
            'mensagem': f'Planilha carregada com sucesso! {len(customer_ids)} registros processados.',
            'dados': {
                'registros_processados': len(customer_ids),
                'planilha_id': planilha_info['id'],
                'data_planilha': data_atual
            }
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro no upload: {str(e)}'}), 500

@app.route('/api/consultar/<customer_id>')
def consultar_customer(customer_id):
    try:
        if customer_id not in customers_data:
            return jsonify({
                'encontrado': False,
                'mensagem': f'Customer ID {customer_id} não encontrado em nenhuma planilha'
            })
        
        customer = customers_data[customer_id]
        
        # Determinar mensagem
        if customer['ativo']:
            mensagem = f'Customer ID {customer_id} está ATIVO na última planilha carregada.'
        else:
            mensagem = f'Customer ID {customer_id} participou da campanha, mas não está mais ativo desde {customer["data_saida"]}.'
        
        # Criar histórico
        historico = [{
            'planilha': 'Planilha carregada',
            'data_entrada': customer['data_entrada'],
            'data_saida': customer['data_saida'],
            'ativo': customer['ativo'],
            'data_upload': customer['data_entrada']
        }]
        
        return jsonify({
            'encontrado': True,
            'customer_id': customer_id,
            'ativo_atual': customer['ativo'],
            'mensagem': mensagem,
            'historico': historico,
            'total_planilhas': len(customer['planilhas']) if 'planilhas' in customer else 1
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro na consulta: {str(e)}'}), 500

@app.route('/api/planilhas')
def listar_planilhas():
    try:
        return jsonify({'planilhas': planilhas_carregadas})
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar planilhas: {str(e)}'}), 500

@app.route('/api/estatisticas')
def estatisticas():
    try:
        total_planilhas = len(planilhas_carregadas)
        total_customers = len(customers_data)
        customers_ativos = sum(1 for c in customers_data.values() if c['ativo'])
        
        ultima_planilha = planilhas_carregadas[-1] if planilhas_carregadas else None
        
        return jsonify({
            'total_planilhas': total_planilhas,
            'total_customers': total_customers,
            'customers_ativos': customers_ativos,
            'ultima_planilha': {
                'data': ultima_planilha['data_upload'] if ultima_planilha else None,
                'arquivo': ultima_planilha['nome_arquivo'] if ultima_planilha else None,
                'registros': ultima_planilha['quantidade_registros'] if ultima_planilha else 0
            }
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar estatísticas: {str(e)}'}), 500

@app.route('/api/relatorio')
def gerar_relatorio():
    try:
        # Criar relatório simples
        relatorio = []
        for customer_id, data in customers_data.items():
            relatorio.append({
                'customer_id': customer_id,
                'data_entrada': data['data_entrada'],
                'data_saida': data['data_saida'] or 'Ativo',
                'status': 'Ativo' if data['ativo'] else 'Inativo'
            })
        
        return jsonify({
            'relatorio': relatorio,
            'total_customers': len(relatorio)
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar relatório: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 