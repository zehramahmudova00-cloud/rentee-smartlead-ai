import { tumLeadler } from 'backend/leads.web';

$w.onReady(function () {
  $w('#html1').onMessage(async (event) => {
    if (event.data?.type !== 'getLeads') return;
    try {
      const result = await tumLeadler();
      $w('#html1').postMessage({ type: 'leadResult', result });
    } catch (_) {
      $w('#html1').postMessage({
        type: 'leadResult',
        result: { basari: false, hata: 'Bu panel yalnızca site yöneticilerine açıktır.' }
      });
    }
  });
});
