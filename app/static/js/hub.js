// app/static/js/hub.js
document.addEventListener('DOMContentLoaded', () => {
  // 1) Intercepta todos os formulários pra não submetê-los antes do WS
  document.querySelectorAll('form').forEach(f => {
    f.addEventListener('submit', e => {
      if (ws.readyState !== WebSocket.OPEN) {
        e.preventDefault();
        alert('Aguarde a conexão com o servidor ser estabelecida...');
      }
    });
  });

  // 2) Função para recalcular visual de faltas
  function recalcStatusIndicators() {
    document.querySelectorAll('.materia-card').forEach(card => {
      const statusIndicator = card.querySelector('.status-indicator');
      if (!statusIndicator) return;
      const txt = statusIndicator.parentElement.textContent;
      const faltas = +(txt.match(/Faltas:\s*(\d+)/) || [0,0])[1];
      const limite = +(txt.match(/\/\s*(\d+)/)   || [0,0])[1];
      statusIndicator.className = 'status-indicator';
      if (faltas > limite)          statusIndicator.classList.add('reprovado');
      else if (faltas > limite * 0.7) statusIndicator.classList.add('recuperacao');
      else                            statusIndicator.classList.add('aprovado');
    });
  }

  // 3) Abre WebSocket
  const protocol = location.protocol === 'https:' ? 'wss://' : 'ws://';
  const ws = new WebSocket(`${protocol}${location.host}/ws`);

  ws.addEventListener('open', () => {
    const mat = document.cookie.match(/(?:^|; )session_id=([^;]+)/)[1];
    ws.send(JSON.stringify({ session_id: mat }));
  });

  ws.addEventListener('message', ({ data }) => {
    const { event, data: d } = JSON.parse(data);
    console.log('WS →', event, d);

    switch (event) {
      case 'falta_incrementada':
      case 'falta_decrementada':
        // atualiza o <span> do resumo
        const res = document.getElementById(`faltas-resumo-${d.codigo}`);
        if (res) res.textContent = d.faltas;
        // atualiza o <span> do card
        const card = document.getElementById(`faltas-card-${d.codigo}`);
        if (card) card.textContent = d.faltas;
        recalcStatusIndicators();
        break;
        
      case 'nova_materia':
      case 'materia_editada':
      case 'materia_excluida':
      case 'nota_adicionada':
      case 'nota_excluida':
      case 'avaliacao_adicionada':
      case 'avaliacao_excluida':
        location.reload();
        break;
    }
  });

  ws.addEventListener('error', err => console.error('WS error', err));
  ws.addEventListener('close', () => console.warn('WS desconectado'));

  // 4) inicializa cores etc.
  recalcStatusIndicators();
});
