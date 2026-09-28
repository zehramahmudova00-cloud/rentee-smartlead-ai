import { fetch } from 'wix-fetch';

const API = 'https://PROJENIZ.onrender.com/api';

$w.onReady(async function () {
  $w('#leadRepeater').onItemReady(($item, itemData) => {
    $item('#isimMetni').text = itemData.isim;
    $item('#telefonMetni').text = itemData.telefon;
    $item('#ilgiMetni').text = itemData.ilgi_alani || '-';
    $item('#tarihMetni').text = itemData.tarih;
  });

  try {
    const response = await fetch(`${API}/leads`);
    const data = await response.json();
    if (!data.basari) throw new Error(data.hata);

    $w('#leadRepeater').data = data.leadler.map((lead) => ({
      ...lead,
      _id: String(lead.id)
    }));

  } catch (error) {
    $w('#panelDurum').text = 'Lead kayıtları getirilemedi.';
  }
});
