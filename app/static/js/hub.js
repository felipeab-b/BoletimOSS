document.querySelectorAll('.materia-card').forEach(card => {
    const faltasElem = card.querySelector('.faltas-warning');
    const statusIndicator = card.querySelector('.status-indicator');
    const limite = parseFloat(statusIndicator.nextSibling.textContent.match(/\/ (\d+)/)[1]);
    const faltas = parseFloat(faltasElem ? faltasElem.textContent : statusIndicator.nextSibling.textContent.match(/: (\d+)/)[1]);
            
    if (faltas > limite) {
        statusIndicator.className = 'status-indicator reprovado';
    } 
    else if (faltas > limite * 0.7) {
        statusIndicator.className = 'status-indicator recuperacao';
    } 
    else {
        statusIndicator.className = 'status-indicator aprovado';
    }
        });
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-btn, .delete-item-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });
});