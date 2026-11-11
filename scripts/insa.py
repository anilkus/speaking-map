"""Şablonlara veriyi ve d3-force'u gömerek sayfaları üretir."""
import sys
d3 = open("d3force.min.js", encoding="utf-8").read()
seq = open("seq.json", encoding="utf-8").read()
t = open("nutuk_sablon.html", encoding="utf-8").read()
open("../nutuk.html", "w", encoding="utf-8").write(t.replace("__D3__", d3).replace("__DATA__", seq).replace("�", ""))
import datetime
t = open("canli_sablon.html", encoding="utf-8").read().replace("__D3__", d3).replace("__VER__", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
open("../canli.html", "w", encoding="utf-8").write(t)
# Türkçe konuş sayfası: aynı şablon, data-mode="turkce"
import re
tr = t.replace('<html lang="tr">', '<html lang="tr" data-mode="turkce">', 1)
tr = tr.replace("<title>Speaking Map · Konuştukça oluşan ağ</title>", "<title>Speaking Map · Türkçe konuş</title>", 1)
tr = tr.replace("<h1>Konuştukça oluşan kelime ağı</h1>", "<h1>Türkçe konuş</h1>", 1)
tr = re.sub(r'<div class="sub">.*?</div>', '<div class="sub">Konuş ya da bir dosya ekle. Türkçe karşılığı olan yabancı kelimeler haritada büyük kırmızı düğüm olarak öne çıkar, altında Türkçesi yazar. Öneriler TDK\'nin Yabancı Sözlere Karşılıklar çalışması ve yaygın kullanım esas alınarak derlendi.</div>', tr, count=1, flags=re.S)
open("../turkce.html", "w", encoding="utf-8").write(tr)
