// app/static/js/hub.js
document.addEventListener('DOMContentLoaded', () => {
  // 0) Pega o session_id do cookie
  const match = document.cookie.match(/(?:^|; )session_id=([^;]+)/);
  const sessionId = match && decodeURIComponent(match[1]);
  if (!sessionId) {
    console.warn('[hub.js] sem session_id no cookie → abortando WS');
    return;
  }

  // 1) Abre a conexão WebSocket (ws:// ou wss:// conforme o protocolo)
  const proto = location.protocol === 'https:' ? 'wss://' : 'ws://';
  const ws = new WebSocket(`${proto}${location.host}/ws`);

  // Função que vai recalcular o indicador de faltas (você já tinha)
  function recalcStatusIndicators() {
    document.querySelectorAll('.materia-card').forEach(card => {
      const statusIndicator = card.querySelector('.status-indicator');
      if (!statusIndicator) return;
      const txt = statusIndicator.parentElement.textContent;
      const fMatch = txt.match(/Faltas:\s*(\d+)/);
      const lMatch = txt.match(/\/\s*(\d+)/);
      const faltas = fMatch ? +fMatch[1] : 0;
      const limite = lMatch ? +lMatch[1] : 0;
      statusIndicator.className = 'status-indicator';
      if (faltas > limite)           statusIndicator.classList.add('reprovado');
      else if (faltas > limite * 0.7) statusIndicator.classList.add('recuperacao');
      else                            statusIndicator.classList.add('aprovado');
    });
  }

  // 2) Ao abrir WS, faz handshake *e* busca eventos pendentes
  ws.addEventListener('open', () => {
    console.log('[hub.js] WS conectado, enviando session_id');
    ws.send(JSON.stringify({ session_id: sessionId }));

    // busca tudo que ficou no buffer antes da conexão
    fetch('/pending_events')
      .then(res => res.json())
      .then(json => {
        json.events.forEach(raw => {
          // simula recebimento pelo WS
          ws.dispatchEvent(new MessageEvent('message', { data: raw }));
        });
      })
      .catch(console.error);
  });

  ws.addEventListener('error', err => {
    console.error('[hub.js] WS error:', err);
  });

  // 3) Trata todas as mensagens do servidor
  ws.addEventListener('message', ({ data }) => {
    let msg;
    try { msg = JSON.parse(data) }
    catch (e) { return console.error('[hub.js] JSON inválido:', data) }

    console.log('[hub.js] evento →', msg.event, msg.data);
    const { event: tipo, data: d } = msg;

    switch (tipo) {
      case 'falta_incrementada':
      case 'falta_decrementada': {
        const el = document.getElementById(`faltas-${d.codigo}`);
        if (el) el.textContent = d.faltas;
        recalcStatusIndicators();
        break;
      }
      default:
        // para qualquer outro evento, basta recarregar a lista
        location.reload();
        break;
    }
  });

  // 4) Recalcula no carregamento inicial
  recalcStatusIndicators();

  // 5) (Opcional) bloqueia submit de form enquanto WS não estiver OPEN
  document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', e => {
      if (ws.readyState !== WebSocket.OPEN) {
        e.preventDefault();
        alert('Aguarde a conexão com o servidor...');
      }
    });
  });
});
