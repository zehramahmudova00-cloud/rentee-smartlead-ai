import { fetch } from 'wix-fetch';

const API = 'https://rentee-smartlead-ai.onrender.com/api';

$w.onReady(function () {
  $w('#sorButonu').onClick(async () => {
    $w('#cevapMetni').text = 'Yanıt hazırlanıyor...';
    try {
      const response = await fetch(`${API}/sohbet`, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mesaj: $w('#mesajInput').value, gecmis: [] })
      });
      const data = await response.json();
      $w('#cevapMetni').text = data.basari ? data.cevap : data.hata;
    } catch (error) {
      $w('#cevapMetni').text = 'Asistana şu anda ulaşılamıyor.';
    }
  });

  $w('#kaydetButonu').onClick(async () => {
    try {
      const response = await fetch(`${API}/leads`, {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          isim: $w('#isimInput').value,
          telefon: $w('#telefonInput').value,
          mesaj: $w('#mesajInput').value,
          ilgi_alani: $w('#ilgiInput').value
        })
      });
      const data = await response.json();
      $w('#formDurum').text = data.basari ? data.mesaj : data.hata;
    } catch (error) {
      $w('#formDurum').text = 'Bilgiler kaydedilemedi.';
    }
  });
});
