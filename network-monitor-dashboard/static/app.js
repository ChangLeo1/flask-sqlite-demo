const refreshButton = document.getElementById('refreshButton');
const lastRefresh = document.getElementById('lastRefresh');
const onlineCount = document.getElementById('onlineCount');
const averageLatency = document.getElementById('averageLatency');

function text(value, suffix = '') {
  return value === null || value === undefined ? '—' : `${value}${suffix}`;
}

function setCard(result) {
  const card = document.querySelector(`[data-target-id="${result.id}"]`);
  if (!card) return;

  card.classList.remove('loading', 'online', 'offline');
  card.classList.add(result.online ? 'online' : 'offline');

  const badge = card.querySelector('.status-badge');
  badge.textContent = result.online ? 'Online' : 'Offline';

  card.querySelector('[data-field="latency"]').textContent = text(result.latency_ms, ' ms');
  card.querySelector('[data-field="loss"]').textContent = text(result.packet_loss, '%');
  card.querySelector('[data-field="dns"]').textContent = result.dns_ip || 'Failed';
  card.querySelector('[data-field="port"]').textContent =
    result.port === null ? 'Not configured' : (result.port_open ? `${result.port} open` : `${result.port} closed`);
  card.querySelector('[data-field="uptime"]').textContent = text(result.uptime_percent, '%');
  card.querySelector('[data-field="error"]').textContent = result.error || '';
}

async function refreshStatus() {
  refreshButton.disabled = true;
  refreshButton.textContent = 'Checking…';

  try {
    const response = await fetch('/api/status', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();

    data.targets.forEach(setCard);
    const online = data.targets.filter(item => item.online).length;
    const latencies = data.targets.map(item => item.latency_ms).filter(value => typeof value === 'number');

    onlineCount.textContent = `${online}/${data.targets.length}`;
    averageLatency.textContent = latencies.length
      ? `${(latencies.reduce((a, b) => a + b, 0) / latencies.length).toFixed(1)} ms`
      : '—';
    lastRefresh.textContent = new Date().toLocaleTimeString();
  } catch (error) {
    lastRefresh.textContent = 'Refresh failed';
    console.error(error);
  } finally {
    refreshButton.disabled = false;
    refreshButton.textContent = 'Run checks now';
  }
}

refreshButton.addEventListener('click', refreshStatus);
refreshStatus();
setInterval(refreshStatus, 30000);
