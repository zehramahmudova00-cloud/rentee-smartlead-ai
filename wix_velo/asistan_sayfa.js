import { fetch } from 'wix-fetch';

const API = 'https://rentee-smartlead-ai.onrender.com/api';

$w.onReady(function () {
  $w('#html1').onMessage(async (event) => {
    const { type, payload, requestId } = event.data || {};
    if (!['sohbet', 'leads'].includes(type)) return;
    try {
      const response = await fetch(`${API}/${type}`, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await response.json();
      $w('#html1').postMessage({ requestId, result });
    } catch (error) {
      $w('#html1').postMessage({
        requestId,
        result: { basari: false, hata: 'Bağlantı kurulamadı. Lütfen tekrar deneyin.' }
      });
    }
  });
});
