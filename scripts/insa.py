"""Şablonlara veriyi ve d3-force'u gömerek sayfaları üretir."""
import sys
d3 = open("d3force.min.js", encoding="utf-8").read()
seq = open("seq.json", encoding="utf-8").read()
t = open("nutuk_sablon.html", encoding="utf-8").read()
open("../nutuk.html", "w", encoding="utf-8").write(t.replace("__D3__", d3).replace("__DATA__", seq).replace("�", ""))
t = open("canli_sablon.html", encoding="utf-8").read()
open("../canli.html", "w", encoding="utf-8").write(t.replace("__D3__", d3))
