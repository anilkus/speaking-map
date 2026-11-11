# Speaking Map

Konuşmayı, söylendikçe büyüyen bir kelime ağına çeviren etkileşimli görselleştirmeler: Atatürk'ün **Nutuk**'u (1919-1927) üzerine üç sayfa ve mikrofonla konuştukça kendi kelime ağını kuran canlı bir sürüm.

**Canlı site:** https://anilkus.github.io/speaking-map/

| Sayfa | Ne yapar |
|---|---|
| [`nutuk.html`](nutuk.html) | Nutuk'u cümle cümle "konuşturur". Kelimeler ilk söylendiklerinde düğüm olarak doğar, aynı cümlede geçen kelimeler bağlanır. 1× hız gerçek konuşma temposudur (Nutuk ~36 saatte okunmuştu). |
| [`canli.html`](canli.html) | Mikrofondan konuşmayı dinler, konuştukça kelime ağını anlık kurar. Türkçe ve İngilizce. Ayrıca metin, belge (.pdf, .docx, .txt), altyazı (.srt, .vtt) ya da ses/video dosyası eklenebilir. |
| [`turkce.html`](turkce.html) | **Türkçe konuş:** konuşmadaki (ya da eklenen dosyadaki) yabancı kökenli kelimeleri haritada büyük kırmızı düğüm olarak gösterir, altına Türkçe karşılığını yazar, anlık uyarı verir ve Türkçe oranını hesaplar. |
| [`kelime-bulutu.html`](kelime-bulutu.html) | En sık geçen 180 kelimenin bulutu ve tablosu; kelimeye tıklayınca örnek cümleler. |

## Yöntem

1. **Metin:** Nutuk tam metni (hafif sadeleştirilmiş bir baskının OCR'lı hali). Satır sonu tireleri ve dipnot numaraları temizlendi.
2. **Lemmatizasyon:** [zeyrek](https://github.com/obulat/zeyrek) (Zemberek'in Python portu) ile her kelime köküne/lemmasına indirildi ("milletin, millete, milleti" → *millet*).
3. **Filtre:** Bağlaçlar, zamirler, yardımcı fiiller ve çok genel kelimeler çıkarıldı.
4. **Ağ:** En sık 150 kelime düğüm; aynı cümlede birlikte geçme sayısı bağ ağırlığı. Okunabilirlik için en güçlü 220 bağ ve her düğümün en güçlü 3 bağı çizilir.
5. **Yerleşim:** [d3-force](https://github.com/d3/d3-force) (sayfalara gömülü).

Canlı sürümde kök bulma tarayıcıda çalışan kural tabanlı bir ek ayıklayıcıyla yapılır: önce fiil ekleri (-ıyor, -acak, -dığı, -mış, edilgen -ıl...), sonra isim ekleri Türkçe sıralamasıyla katman katman (hal → iyelik → çoğul) sökülür. Aynı kelimenin farklı hallerinin aynı köke gitmesi için daha önce görülen köklerle eşleştirme yapılır; ünsüz yumuşaması (kitap/kitabı, renk/rengi) ve ünlü düşmesi (isim/ismi) de hesaba katılır. "vardı, dediğimiz, biliyorsunuz, etmiştir" gibi yardımcı fiil çekimleri ağa alınmaz. Birbirine yakın söylenen kelimeler (6 kelimelik pencere) bağlanır.

İsimler de birleştirilir: küçük harfle tanınan haller ("turkcell" → Turkcell), türev halleri ("Galatasaraylı" → Galatasaray) ve tam adın kısmi geçişleri ("Bozok Üniversitesi" → Yozgat Bozok Üniversitesi, "Anıl" → Anıl Kuş, tek bir eşleşme varsa) aynı düğümde toplanır.

## Canlı sürüm hakkında

- Konuşma tanıma tarayıcının yerleşik **Web Speech API**'si ile yapılır: Chrome, Edge ve Safari'de çalışır, Firefox'ta çalışmaz.
- Chrome'da ses, metne çevrilmek üzere Google'ın sunucularına gönderilir. Oluşan kelimeler ve ağ yalnızca tarayıcıda tutulur, hiçbir yere kaydedilmez.
- Mikrofon yalnızca https üzerinden (GitHub Pages gibi) veya `localhost`'ta çalışır.
- Süre sınırı yok: tarayıcı tanıma oturumunu kapattığında sayfa otomatik yeniden başlatır. Kelime sayısı da sınırsız; ekranda en sık 130 kelime gösterilir, geri kalanı arka planda sayılmaya devam eder.

## Dosya, belge, ses ve video eklemek

**＋ Dosya / metin** düğmesiyle ya da dosyayı sayfaya sürükleyerek:

- **Metin ve belgeler:** .txt, .md, .pdf ([pdf.js](https://mozilla.github.io/pdf.js/)), .docx ([mammoth](https://github.com/mwilliamson/mammoth.js)). Taranmış (görüntü) PDF'lerde metin olmadığı için çalışmaz.
- **Altyazılar:** .srt, .vtt (zaman damgaları ve etiketler temizlenir). YouTube videolarının altyazısını indirip buradan yükleyebilirsin.
- **Ses ve video:** .mp3, .wav, .m4a, .mp4, .webm, .mov... Ses, [Transformers.js](https://github.com/huggingface/transformers.js) ile tarayıcıda çalışan **Whisper** modeliyle yazıya dökülür; dosya hiçbir sunucuya gönderilmez. Model ilk kullanımda Hugging Face'ten indirilir (tiny ~40 MB, base ~80 MB, small ~250 MB) ve tarayıcıda saklanır. Ses 60 saniyelik bloklar halinde işlenir, ağ her blok yazıya döküldükçe büyür. Hız bilgisayara bağlıdır; uzun kayıtlarda bekleme süresi gösterilir ve işlem iptal edilebilir. En fazla 700 MB.

## Türkçe konuş

`turkce.html`, canlı sayfayla aynı motoru kullanır; ek olarak:

- **Sözlük:** yaklaşık 280 kelimelik elle derlenmiş bir karşılıklar listesi. TDK'nin *Yabancı Sözlere Karşılıklar Kılavuzu* çalışması ve yaygın kullanım esas alınmıştır. TDK'nin ilkesine uygun olarak Türkçeye çoktan yerleşmiş kelimelere (televizyon, kitap, ofis...) karşılık önerilmez.
- **İki düzey:** Batı kökenli, yerleşmemiş kelimeler (meeting → toplantı, feedback → geri bildirim, spesifik → belirli) kırmızı; eski Arapça/Farsça kullanımlar (istikbal → gelecek, mütemadiyen → sürekli) pembe ve isteğe bağlı. Kapsam menüden "Yalnız Batı kökenli" yapılabilir.
- **Ekli halleri tanır:** "meeting'de", "feedback'lerinizi", "konsepti", "update'leri", "focuslanmak".
- Sözlükte olmayan ama İngilizce yazımlı görünen kelimeler (w, x, q, th, -ing...) "yabancı olabilir" diye işaretlenir.
- Anlık uyarı ("'meeting' yerine **toplantı** diyebilirsin"), canlı "Türkçesi varken" paneli, Türkçe oranı ve raporda öneri listesi.

## Konuşma raporu

Canlı sayfada **📊 Rapor** (mikrofon durdurulunca otomatik açılır) şunları verir:

- **Otomatik özet:** konuşmayı en iyi temsil eden 3, 5 ya da 8 cümle, özgün sırasıyla. Kelime ağına PageRank uygulanır (TextRank, Mihalcea ve Tarau 2004), cümleler içerdikleri merkezi kelimelere göre puanlanır (Luhn 1958) ve birbirini tekrar eden cümleler elenir (MMR, Carbonell ve Goldstein 1998). Ayrıca her konu kümesi için onu en iyi temsil eden bir cümle seçilir.
- **Sayılar:** toplam/anlamlı kelime, farklı kök sayısı, konuşma hızı (kelime/dk, yalnız mikrofonda), kelime çeşitliliği (MATTR, 100 kelimelik kayan pencere), dinleme süresi
- **Konu kümeleri:** kelimeler birlikte geçme benzerliğine (kosinüs, her kelime için en yakın 6 komşu) göre Louvain yöntemiyle kümelenir; **Kümeler** düğmesi ağı bu kümelere göre renklendirir
- **Çıkarımlar:** ana eksen, konu sayısı, farklı konuları bağlayan köprü kelime, konuşmanın akışı (başta / ortada / sonda öne çıkan kelimeler), çeşitlilik ve hız yorumu, dolgu kelime oranı ("yani", "işte", "şey"...)
- **En sık kelimeler, en güçlü bağlar** ve en merkezi kelimeler (PageRank)
- Rapor Markdown olarak kopyalanabilir ya da indirilebilir

Çıkarımlar kural tabanlıdır (eşikler yaklaşık değerlerdir), herhangi bir yapay zekâ servisine veri gönderilmez.

## Özel isimler, yerler ve kalıp ifadeler

Canlı sayfa kelimeleri dört tipe ayırır, ağda her tip ayrı şekil ve renkle çizilir:

| Tip | Nasıl bulunur | Şekil |
|---|---|---|
| **Yer** | Gömülü liste: 81 il, bilinen ilçeler, ülkeler, bölgeler ve büyük dünya şehirleri (ekli halleri de: "Ankara'da", "İzmir'e") | yeşil kare |
| **Kişi / kurum / marka** | Cümle ortasında büyük harfle başlayan, kesme işaretiyle ek almış ya da tamamı büyük harf olan kelimeler (Google, TÜBİTAK, OpenAI). Art arda gelen isimler tek düğüm olur ("Mustafa Kemal Atatürk", "Yozgat Bozok Üniversitesi"); "Prof.", "Dr." gibi unvanlar atlanır | sarı baklava |
| **Kalıp ifade** | En az 3 kez yan yana geçen ve çoğunlukla birlikte kullanılan kelime ikilileri otomatik birleşir ("yapay zekâ", "dil modelleri") | mor altıgen |
| **Kelime** | Diğer her şey | mavi daire |

Raporda "Bahsedilen yerler", "Kişi, kurum ve markalar" ve "Kalıp ifadeler" bölümleri bunları sayılarıyla listeler.

Sınırlamalar: tespit, konuşma tanıma motorunun büyük harf ve kesme işareti kullanımına dayanır. Cümlenin ilk kelimesi olan tek kelimelik isimler (ör. cümle başında "Meta") ancak konuşmada bir kez daha cümle ortasında geçtikten sonra isim olarak tanınır. Kişi, kurum ve marka birbirinden ayrılmaz. "Ordu", "Van", "Tokat" gibi aynı zamanda sıradan kelime olan il adları yalnızca büyük harfle ve cümle ortasında yazıldığında yer sayılır.

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
