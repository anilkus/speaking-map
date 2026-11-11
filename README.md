# Speaking Map

Konuşmayı, söylendikçe büyüyen bir kelime ağına çeviren etkileşimli görselleştirmeler: Atatürk'ün **Nutuk**'u (1919-1927) üzerine üç sayfa ve mikrofonla konuştukça kendi kelime ağını kuran canlı bir sürüm.

**Canlı site:** https://anilkus.github.io/speaking-map/

| Sayfa | Ne yapar |
|---|---|
| [`nutuk.html`](nutuk.html) | Nutuk'u cümle cümle "konuşturur". Kelimeler ilk söylendiklerinde düğüm olarak doğar, aynı cümlede geçen kelimeler bağlanır. 1× hız gerçek konuşma temposudur (Nutuk ~36 saatte okunmuştu). |
| [`canli.html`](canli.html) | Mikrofondan konuşmayı dinler, konuştukça kelime ağını anlık kurar. Türkçe ve İngilizce. Mikrofon yoksa metin yapıştırıp oynatılabilir. |
| [`kelime-bulutu.html`](kelime-bulutu.html) | En sık geçen 180 kelimenin bulutu ve tablosu; kelimeye tıklayınca örnek cümleler. |

## Yöntem

1. **Metin:** Nutuk tam metni (hafif sadeleştirilmiş bir baskının OCR'lı hali). Satır sonu tireleri ve dipnot numaraları temizlendi.
2. **Lemmatizasyon:** [zeyrek](https://github.com/obulat/zeyrek) (Zemberek'in Python portu) ile her kelime köküne/lemmasına indirildi ("milletin, millete, milleti" → *millet*).
3. **Filtre:** Bağlaçlar, zamirler, yardımcı fiiller ve çok genel kelimeler çıkarıldı.
4. **Ağ:** En sık 150 kelime düğüm; aynı cümlede birlikte geçme sayısı bağ ağırlığı. Okunabilirlik için en güçlü 220 bağ ve her düğümün en güçlü 3 bağı çizilir.
5. **Yerleşim:** [d3-force](https://github.com/d3/d3-force) (sayfalara gömülü).

Canlı sürümde lemmatizasyon tarayıcıda çalışan basit bir ek ayıklayıcıyla yapılır; birbirine yakın söylenen kelimeler (6 kelimelik pencere) bağlanır.

## Canlı sürüm hakkında

- Konuşma tanıma tarayıcının yerleşik **Web Speech API**'si ile yapılır: Chrome, Edge ve Safari'de çalışır, Firefox'ta çalışmaz.
- Chrome'da ses, metne çevrilmek üzere Google'ın sunucularına gönderilir. Oluşan kelimeler ve ağ yalnızca tarayıcıda tutulur, hiçbir yere kaydedilmez.
- Mikrofon yalnızca https üzerinden (GitHub Pages gibi) veya `localhost`'ta çalışır.
- Süre sınırı yok: tarayıcı tanıma oturumunu kapattığında sayfa otomatik yeniden başlatır. Kelime sayısı da sınırsız; ekranda en sık 130 kelime gösterilir, geri kalanı arka planda sayılmaya devam eder.

## Konuşma raporu

Canlı sayfada **📊 Rapor** (mikrofon durdurulunca otomatik açılır) şunları verir:

- **Özet:** toplam/anlamlı kelime, farklı kök sayısı, konuşma hızı (kelime/dk, yalnız mikrofonda), kelime çeşitliliği (MATTR, 100 kelimelik kayan pencere), dinleme süresi
- **Konu kümeleri:** kelimeler birlikte geçme benzerliğine (kosinüs, her kelime için en yakın 6 komşu) göre Louvain yöntemiyle kümelenir; **Kümeler** düğmesi ağı bu kümelere göre renklendirir
- **Çıkarımlar:** ana eksen, konu sayısı, farklı konuları bağlayan köprü kelime, konuşmanın akışı (başta / ortada / sonda öne çıkan kelimeler), çeşitlilik ve hız yorumu, dolgu kelime oranı ("yani", "işte", "şey"...)
- **En sık kelimeler, en güçlü bağlar** ve en çok bağlantı kuran kelimeler
- Rapor Markdown olarak kopyalanabilir ya da indirilebilir

Çıkarımlar kural tabanlıdır (eşikler yaklaşık değerlerdir), herhangi bir yapay zekâ servisine veri gönderilmez.

## Yeniden üretmek

```bash
pip install zeyrek
cd scripts
python frekans.py nutuk.txt freq.json        # frekanslar
python kategoriler.py freq.json freq2.json   # kategoriler
python cumle_dizisi.py nutuk.txt seq.json freq2.json   # cümle başına kelime dizisi
python insa.py                               # sayfaları üretir (d3force.min.js ve seq.json gerekir)
```

## Lisans

Kod: MIT. Nutuk metni kamu malıdır; kullanılan baskının sadeleştirmesi ve OCR hataları ilgili kaynağa aittir.

Hazırlayan: [Anıl Kuş](https://anilkus.github.io/)
