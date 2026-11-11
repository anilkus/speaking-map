"""Türkçe konuş sayfası için İngilizce-baskın kelime listesini ve Türkçe istisnaları üretir.

Kaynak: hermitdave/FrequencyWords (OpenSubtitles 2018), içerik CC BY-SA 4.0.
  en_50k.txt: https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/en/en_50k.txt
  tr_50k.txt: https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/tr/tr_50k.txt
Kural: kelime İngilizcede Türkçeye göre en az 8 kat sık geçiyorsa yabancı sayılır; ancak Türkçede
milyonda 30'dan sık geçiyorsa ya da Türkçe ekli halleri (canım, boyunca...) listede varsa Türkçe kabul edilir.
Çıktı: en_dom.json, trx.json (Türkçe olduğu halde ek ayırınca İngilizceye benzeyen kelimeler).
"""
import json, re
def load(f):
    d = {}; tot = 0
    for l in open(f, encoding="utf-8"):
        w, c = l.rsplit(" ", 1); c = int(c); d[w] = c; tot += c
    return d, tot
en, et = load("en_50k.txt"); tr, tt = load("tr_50k.txt")
S = ["ı","i","u","ü","a","e","da","de","dan","den","ta","te","tan","ten","lar","ler","ın","in","un","ün","nın","nin","yı","yi","ya","ye","ım","im","um","üm","ları","leri","larda","lerde","dır","dir","du","dı","sı","si","su","sü","unu","ını","ini","ünü","unca","ınca","ince"]
out = []
for i, (w, c) in enumerate(en.items()):
    if i >= 40000: break
    if len(w) < 3 or not re.fullmatch(r"[a-z]+", w): continue
    e = en[w] / et * 1e6; t = tr.get(w, 0) / tt * 1e6
    if e / (t + 0.05) < 8: continue
    if t >= 30 or sum(1 for s in S if (w + s) in tr) >= 3: continue
    out.append(w)
endom = set(out)
L1 = ["ndaki","ndeki","ndan","nden","daki","deki","taki","teki","dan","den","tan","ten","nda","nde","nın","nin","nun","nün","yla","yle","da","de","ta","te","ın","in","un","ün","la","le","ya","ye","na","ne","yı","yi","yu","yü","ı","i","u","ü","a","e"]
L2 = ["ımız","imiz","umuz","ümüz","ınız","iniz","unuz","ünüz","ları","leri","sı","si","su","sü","ı","i","u","ü"]
L3 = ["lar","ler"]
ANY = set(L1 + L2 + L3 + [b + a for a in L1 for b in L2] + [b + a for a in L1 for b in L3] + [b + a for a in L2 for b in L3] + ["ma","me","mak","mek","ması","mesi"])
EXT = re.compile(r"^(l[ae](n|ş|t|y)?|d[ıiuü]r|s[ıiuü]n|[ıiuü]m|[ıiuü]z|t[ıiuü]|d[ıiuü])")
def hit(w):
    if w in endom: return w
    for cut in range(1, 7):
        if len(w) - cut < 4: break
        b, rest = w[:-cut], w[-cut:]
        if b in endom and (rest in ANY or EXT.match(rest)): return b
trx = [w for w, c in tr.items() if c / tt * 1e6 >= 0.3 and w not in endom and hit(w)]
json.dump(out, open("en_dom.json", "w")); json.dump(sorted(trx), open("trx.json", "w"), ensure_ascii=False)
print(len(out), "yabancı,", len(trx), "istisna")
