#!/usr/bin/env python3
"""
Sistema Simples de Importação CSV e Consulta de Customer ID
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os
import io
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customer_tracking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Modelos do banco de dados
class Planilha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    quantidade_registros = db.Column(db.Integer, nullable=False)
    data_planilha = db.Column(db.Date, nullable=False)  # Data da planilha (nome do arquivo ou data de upload)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), nullable=False)
    planilha_id = db.Column(db.Integer, db.ForeignKey('planilha.id'), nullable=False)
    data_entrada = db.Column(db.Date, nullable=False)
    data_saida = db.Column(db.Date, nullable=True)  # Null se ainda ativo
    ativo = db.Column(db.Boolean, default=True)

# Criar tabelas
with app.app_context():
    db.create_all()

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
        
        # Salvar arquivo
        filename = secure_filename(arquivo.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        arquivo.save(filepath)
        
        # Ler CSV
        df = pd.read_csv(filepath)
        
        # Verificar se tem a coluna customer_id
        if 'customer_id' not in df.columns:
            return jsonify({'erro': 'Coluna "customer_id" não encontrada no arquivo'}), 400
        
        # Data da planilha (usar data atual se não especificada)
        data_planilha = datetime.now().date()
        
        # Criar registro da planilha
        planilha = Planilha(
            nome_arquivo=filename,
            quantidade_registros=len(df),
            data_planilha=data_planilha
        )
        db.session.add(planilha)
        db.session.commit()
        
        # Processar registros
        registros_processados = 0
        
        for index, row in df.iterrows():
            customer_id = str(row['customer_id']).strip()
            
            if not customer_id or customer_id == 'nan':
                continue
            
            # Verificar se customer já existe em alguma planilha
            customer_existente = Customer.query.filter_by(
                customer_id=customer_id, 
                ativo=True
            ).first()
            
            if customer_existente:
                # Marcar como inativo na planilha anterior
                customer_existente.ativo = False
                customer_existente.data_saida = data_planilha
            
            # Criar novo registro
            customer = Customer(
                customer_id=customer_id,
                planilha_id=planilha.id,
                data_entrada=data_planilha,
                ativo=True
            )
            db.session.add(customer)
            registros_processados += 1
        
        db.session.commit()
        
        return jsonify({
            'sucesso': True,
            'mensagem': f'Planilha carregada com sucesso!',
            'dados': {
                'registros_processados': registros_processados,
                'planilha_id': planilha.id,
                'data_planilha': data_planilha.strftime('%d/%m/%Y')
            }
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro no upload: {str(e)}'}), 500

@app.route('/api/consultar/<customer_id>')
def consultar_customer(customer_id):
    try:
        # Buscar histórico completo do customer
        historico = Customer.query.filter_by(
            customer_id=customer_id
        ).order_by(Customer.data_entrada.desc()).all()
        
        if not historico:
            return jsonify({
                'encontrado': False,
                'mensagem': f'Customer ID {customer_id} não encontrado em nenhuma planilha'
            })
        
        # Verificar se está ativo na última planilha
        ultimo_registro = historico[0]
        ativo_atual = ultimo_registro.ativo
        
        # Buscar informações das planilhas
        historico_detalhado = []
        for h in historico:
            planilha = Planilha.query.get(h.planilha_id)
            if planilha:
                historico_detalhado.append({
                    'planilha': planilha.nome_arquivo,
                    'data_entrada': h.data_entrada.strftime('%d/%m/%Y'),
                    'data_saida': h.data_saida.strftime('%d/%m/%Y') if h.data_saida else None,
                    'ativo': h.ativo,
                    'data_upload': planilha.data_upload.strftime('%d/%m/%Y %H:%M')
                })
        
        # Determinar mensagem baseada no status
        if ativo_atual:
            mensagem = f'Customer ID {customer_id} está ATIVO na última planilha carregada.'
        else:
            ultima_data = historico_detalhado[0]['data_saida']
            mensagem = f'Customer ID {customer_id} participou da campanha, mas não está mais ativo desde {ultima_data}.'
        
        return jsonify({
            'encontrado': True,
            'customer_id': customer_id,
            'ativo_atual': ativo_atual,
            'mensagem': mensagem,
            'historico': historico_detalhado,
            'total_planilhas': len(historico_detalhado)
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro na consulta: {str(e)}'}), 500

@app.route('/api/planilhas')
def listar_planilhas():
    try:
        planilhas = Planilha.query.order_by(Planilha.data_upload.desc()).all()
        
        dados = []
        for planilha in planilhas:
            # Contar customers ativos nesta planilha
            customers_ativos = Customer.query.filter_by(
                planilha_id=planilha.id, 
                ativo=True
            ).count()
            
            dados.append({
                'id': planilha.id,
                'nome_arquivo': planilha.nome_arquivo,
                'data_upload': planilha.data_upload.strftime('%d/%m/%Y %H:%M'),
                'data_planilha': planilha.data_planilha.strftime('%d/%m/%Y'),
                'quantidade_registros': planilha.quantidade_registros,
                'customers_ativos': customers_ativos
            })
        
        return jsonify({'planilhas': dados})
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao listar planilhas: {str(e)}'}), 500

@app.route('/api/estatisticas')
def estatisticas():
    try:
        total_planilhas = Planilha.query.count()
        total_customers = Customer.query.count()
        customers_ativos = Customer.query.filter_by(ativo=True).count()
        
        # Última planilha
        ultima_planilha = Planilha.query.order_by(Planilha.data_upload.desc()).first()
        
        return jsonify({
            'total_planilhas': total_planilhas,
            'total_customers': total_customers,
            'customers_ativos': customers_ativos,
            'ultima_planilha': {
                'data': ultima_planilha.data_upload.strftime('%d/%m/%Y %H:%M') if ultima_planilha else None,
                'arquivo': ultima_planilha.nome_arquivo if ultima_planilha else None,
                'registros': ultima_planilha.quantidade_registros if ultima_planilha else 0
            }
        })
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao buscar estatísticas: {str(e)}'}), 500

@app.route('/api/relatorio')
def gerar_relatorio():
    try:
        # Buscar todos os customers com histórico
        customers = db.session.query(Customer.customer_id).distinct().all()
        
        # Criar relatório
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Customer ID', 'Data de Entrada', 'Data de Saída', 'Status Atual'])
        
        for (customer_id,) in customers:
            # Buscar primeiro e último registro
            primeiro = Customer.query.filter_by(customer_id=customer_id).order_by(Customer.data_entrada.asc()).first()
            ultimo = Customer.query.filter_by(customer_id=customer_id).order_by(Customer.data_entrada.desc()).first()
            
            data_entrada = primeiro.data_entrada.strftime('%d/%m/%Y')
            data_saida = ultimo.data_saida.strftime('%d/%m/%Y') if ultimo.data_saida else 'Ativo'
            status = 'Ativo' if ultimo.ativo else 'Inativo'
            
            writer.writerow([customer_id, data_entrada, data_saida, status])
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8')),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'relatorio_customers_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({'erro': f'Erro ao gerar relatório: {str(e)}'}), 500

# Para o Vercel
app.debug = False

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 