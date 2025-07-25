// Área Administrativa - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elementos da interface
    const uploadForm = document.getElementById('uploadForm');
    const uploadStatus = document.getElementById('uploadStatus');
    const planilhasContainer = document.getElementById('planilhasContainer');
    const downloadRelatorio = document.getElementById('downloadRelatorio');
    
    // Estatísticas
    const totalPlanilhas = document.getElementById('totalPlanilhas');
    const totalCustomers = document.getElementById('totalCustomers');
    const customersAtivos = document.getElementById('customersAtivos');

    // Carregar dados iniciais
    carregarEstatisticas();
    carregarPlanilhas();

    // Upload de arquivo CSV
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const fileInput = document.getElementById('csvFile');
        const file = fileInput.files[0];
        
        if (!file) {
            mostrarMensagem('Por favor, selecione um arquivo CSV.', 'error');
            return;
        }
        
        if (!file.name.endsWith('.csv')) {
            mostrarMensagem('Por favor, selecione apenas arquivos CSV.', 'error');
            return;
        }
        
        // Mostrar status de upload
        uploadStatus.style.display = 'block';
        document.getElementById('uploadButton').disabled = true;
        
        const formData = new FormData();
        formData.append('arquivo', file);
        
        fetch('/api/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            uploadStatus.style.display = 'none';
            document.getElementById('uploadButton').disabled = false;
            
            if (data.sucesso) {
                const detalhes = data.dados;
                const mensagem = `${data.mensagem}\n\nRegistros processados: ${detalhes.registros_processados}\nNovos customers: ${detalhes.novos_customers}\nCustomers atualizados: ${detalhes.customers_atualizados}`;
                mostrarMensagem(mensagem, 'success');
                uploadForm.reset();
                carregarEstatisticas();
                carregarPlanilhas();
            } else {
                mostrarMensagem(data.erro, 'error');
            }
        })
        .catch(error => {
            uploadStatus.style.display = 'none';
            document.getElementById('uploadButton').disabled = false;
            mostrarMensagem('Erro ao carregar arquivo: ' + error.message, 'error');
        });
    });

    // Download de relatório
    downloadRelatorio.addEventListener('click', function() {
        window.location.href = '/api/relatorio';
    });

    // Função para carregar estatísticas
    function carregarEstatisticas() {
        fetch('/api/estatisticas')
            .then(response => response.json())
            .then(data => {
                totalPlanilhas.textContent = data.total_planilhas;
                totalCustomers.textContent = data.total_customers;
                customersAtivos.textContent = data.customers_ativos;
            })
            .catch(error => {
                console.error('Erro ao carregar estatísticas:', error);
            });
    }

    // Função para carregar planilhas
    function carregarPlanilhas() {
        planilhasContainer.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i><p>Carregando planilhas...</p></div>';
        
        fetch('/api/planilhas')
            .then(response => response.json())
            .then(data => {
                if (data.planilhas && data.planilhas.length > 0) {
                    let html = '';
                    data.planilhas.forEach(planilha => {
                        html += `
                            <div class="planilha-card">
                                <h3><i class="fas fa-file-csv"></i> ${planilha.nome_arquivo}</h3>
                                <p><strong>Data de Upload:</strong> ${planilha.data_upload}</p>
                                <p><strong>Data da Planilha:</strong> ${planilha.data_planilha}</p>
                                <p><strong>Registros:</strong> ${planilha.quantidade_registros}</p>
                                <p><strong>Customers Ativos:</strong> ${planilha.customers_ativos}</p>
                                <span class="status ${planilha.customers_ativos > 0 ? 'ativo' : 'inativo'}">
                                    ${planilha.customers_ativos > 0 ? 'Com Ativos' : 'Sem Ativos'}
                                </span>
                            </div>
                        `;
                    });
                    planilhasContainer.innerHTML = html;
                } else {
                    planilhasContainer.innerHTML = '<div class="loading"><i class="fas fa-info-circle"></i><p>Nenhuma planilha carregada ainda.</p></div>';
                }
            })
            .catch(error => {
                planilhasContainer.innerHTML = '<div class="loading"><i class="fas fa-exclamation-triangle"></i><p>Erro ao carregar planilhas.</p></div>';
                console.error('Erro ao carregar planilhas:', error);
            });
    }

    // Função para mostrar mensagens
    function mostrarMensagem(mensagem, tipo) {
        // Criar elemento de mensagem
        const mensagemDiv = document.createElement('div');
        mensagemDiv.className = `mensagem ${tipo}`;
        mensagemDiv.innerHTML = `
            <div style="position: fixed; top: 20px; right: 20px; z-index: 1000; padding: 15px 20px; border-radius: 10px; color: white; font-weight: 500; max-width: 400px;">
                <i class="fas fa-${tipo === 'success' ? 'check-circle' : tipo === 'error' ? 'times-circle' : 'info-circle'}"></i>
                ${mensagem}
            </div>
        `;
        
        // Aplicar estilo baseado no tipo
        const mensagemElement = mensagemDiv.querySelector('div');
        if (tipo === 'success') {
            mensagemElement.style.background = 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)';
        } else if (tipo === 'error') {
            mensagemElement.style.background = 'linear-gradient(135deg, #f56565 0%, #e53e3e 100%)';
        } else {
            mensagemElement.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
        }
        
        document.body.appendChild(mensagemDiv);
        
        // Remover mensagem após 5 segundos
        setTimeout(() => {
            if (mensagemDiv.parentNode) {
                mensagemDiv.parentNode.removeChild(mensagemDiv);
            }
        }, 5000);
    }

    // Atualizar nome do arquivo selecionado
    document.getElementById('csvFile').addEventListener('change', function(e) {
        const fileName = e.target.files[0]?.name || 'Clique para selecionar arquivo CSV';
        document.querySelector('.file-label span').textContent = fileName;
    });
}); 