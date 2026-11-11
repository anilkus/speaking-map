"""Şablonlara veriyi ve d3-force'u gömerek sayfaları üretir (scripts klasöründen çalıştır)."""
import re, datetime
d3 = open("d3force.min.js", encoding="utf-8").read()
seq = open("seq.json", encoding="utf-8").read()
t = open("nutuk_sablon.html", encoding="utf-8").read()
open("../nutuk.html", "w", encoding="utf-8").write(t.replace("__D3__", d3).replace("__DATA__", seq).replace("�", ""))
# Canlı sayfalar: aynı şablon, üç mod (genel = Konuş, yukle = Sen yükle, turkce = Türkçe konuş)
t = open("canli_sablon.html", encoding="utf-8").read().replace("__D3__", d3).replace("__VER__", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
def page(mode, title, h1, sub):
    p = t.replace('<html lang="tr">', f'<html lang="tr" data-mode="{mode}">', 1)
    p = p.replace("<title>Speaking Map · Konuştukça oluşan ağ</title>", f"<title>{title}</title>", 1)
    p = p.replace("<h1>Konuştukça oluşan kelime ağı</h1>", f"<h1>{h1}</h1>", 1)
    return re.sub(r'<div class="sub">.*?</div>', f'<div class="sub">{sub}</div>', p, count=1, flags=re.S)
open("../canli.html", "w", encoding="utf-8").write(page("genel", "Speaking Map · Konuş", "Konuştukça oluşan kelime ağı", "Mikrofonu aç ve konuş. Söylediğin her anlamlı kelime bir düğüm olur, birbirine yakın söylenen kelimeler bağlanır. Tekrarladıkça düğümler büyür, bağlar kalınlaşır."))
open("../yukle.html", "w", encoding="utf-8").write(page("yukle", "Speaking Map · Sen yükle", "Sen yükle", "Bir belge, altyazı, ses ya da video yükle. İçindeki konuşma okunurken kelime ağına dönüşür, sonunda özet ve rapor çıkar."))
open("../turkce.html", "w", encoding="utf-8").write(page("turkce", "Speaking Map · Türkçe konuş", "Türkçe konuş", "Mikrofonu aç ve konuş. Kullandığın yabancı kelimeler kırmızı ✗ ile, yerine söyleyebileceğin Türkçesi yeşil 👍 ile belirir. Öneriler TDK'nin Yabancı Sözlere Karşılıklar çalışması ve yaygın kullanım esas alınarak derlendi."))
