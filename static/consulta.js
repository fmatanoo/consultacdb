// Área de Consulta Pública - JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elementos da interface
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const resultSection = document.getElementById('resultSection');
    const resultCard = document.getElementById('resultCard');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    const resultMessage = document.getElementById('resultMessage');
    const resultDetails = document.getElementById('resultDetails');

    // Consulta de customer_id
    searchButton.addEventListener('click', function() {
        const customerId = searchInput.value.trim();
        
        if (!customerId) {
            mostrarMensagem('Por favor, digite um customer_id para consultar.', 'error');
            return;
        }
        
        consultarCustomer(customerId);
    });

    // Consulta ao pressionar Enter
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchButton.click();
        }
    });

    // Função para consultar customer
    function consultarCustomer(customerId) {
        resultSection.style.display = 'none';
        
        // Mostrar loading
        resultSection.style.display = 'block';
        resultCard.className = 'result-card';
        resultIcon.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        resultTitle.textContent = 'Consultando...';
        resultMessage.textContent = 'Verificando na base de dados...';
        resultDetails.innerHTML = '';
        
        fetch(`/api/consultar/${customerId}`)
            .then(response => response.json())
            .then(data => {
                if (data.encontrado) {
                    mostrarResultado(data, 'success');
                } else {
                    mostrarResultado(data, 'error');
                }
            })
            .catch(error => {
                mostrarMensagem('Erro na consulta: ' + error.message, 'error');
                resultSection.style.display = 'none';
            });
    }

    // Função para mostrar resultado da consulta
    function mostrarResultado(data, tipo) {
        resultSection.style.display = 'block';
        
        if (tipo === 'success') {
            resultCard.className = 'result-card success';
            resultIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
            resultTitle.textContent = 'Customer Encontrado';
            resultMessage.textContent = data.mensagem;
            
            // Detalhes do histórico
            let detalhesHTML = '<div style="margin-top: 15px;">';
            detalhesHTML += '<strong>Histórico de Planilhas:</strong><br>';
            
            data.historico.forEach((item, index) => {
                const status = item.ativo ? 'Ativo' : 'Inativo';
                const statusClass = item.ativo ? 'ativo' : 'inativo';
                
                detalhesHTML += `
                    <div style="margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.2); border-radius: 8px;">
                        <strong>Planilha ${index + 1}:</strong> ${item.planilha}<br>
                        <strong>Data de Entrada:</strong> ${item.data_entrada}<br>
                        ${item.data_saida ? `<strong>Data de Saída:</strong> ${item.data_saida}<br>` : ''}
                        <strong>Status:</strong> <span class="status ${statusClass}">${status}</span><br>
                        <strong>Upload:</strong> ${item.data_upload}
                    </div>
                `;
            });
            
            detalhesHTML += '</div>';
            resultDetails.innerHTML = detalhesHTML;
            
        } else {
            resultCard.className = 'result-card error';
            resultIcon.innerHTML = '<i class="fas fa-times-circle"></i>';
            resultTitle.textContent = 'Customer Não Encontrado';
            resultMessage.textContent = data.mensagem;
            resultDetails.innerHTML = '';
        }
        
        // Scroll para o resultado
        resultSection.scrollIntoView({ behavior: 'smooth' });
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

    // Focar no campo de busca ao carregar a página
    searchInput.focus();
}); 