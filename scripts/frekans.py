import re, json, sys, logging, collections
logging.disable(logging.CRITICAL)
import zeyrek, zeyrek.morphology as m
m._tokenize_text = lambda t: t.split()

src = sys.argv[1]
raw = open(src, encoding="utf-8").read()

# OCR cleanup: soft-hyphen / hyphen line breaks, odd chars
t = raw.replace("­\n", "").replace("­", "")
t = re.sub(r"(\w)-\n(\w)", r"\1\2", t)
t = t.replace("·", "").replace("’", "'")
t = re.sub(r"\s*\n\s*", " ", t)
t = re.sub(r"\s+", " ", t)

def tr_lower(s):
    return s.replace("I", "ı").replace("İ", "i").lower()

sentences = re.split(r"(?<=[.!?…])\s+", t)

STOP = set("""
ve veya ile ki de da bu şu o bir iki üç her hiç çok daha en pek gibi kadar için diye ama fakat lakin ancak yalnız
ise ya mi mı mu mü ne niçin nasıl neden niye hem dahi bile zaten artık şimdi sonra evvel önce yine tekrar
ben sen biz siz onlar kendi kendisi böyle şöyle öyle bunlar şunlar orada burada şey şeyler bazı birçok diğer başka
olmak etmek bulunmak eylemek demek yapmak vermek almak gelmek gitmek görmek bilmek kalmak istemek çıkmak
var yok değil olarak olan olduğu üzere dair rağmen göre karşı doğru beri itibaren ait aynı tarafından suretle
efendim efendiler mademki halde zaman vakit gün sene hususta husus hakkında suretiyle dolayı ilk son
bunu buna bunun bundan onu ona onun ondan şunu bizim bize bizi sizin size sizi benim bana beni onların
bun günü ederek ede değmek biri basım sözcük hiçbir alınmak eder varmak hal taraf zat beraber bütün bulunmak edilmek olunmak lazım nihayet yani mesela belki elbette hatta üzerine üzerinde arasında içinde altında yanında tarafında
mı mıdır midir dır dir tır tir idi imiş ise iken ola olur olsun olmuş olacak olduğunu
""".split())

an = zeyrek.MorphAnalyzer()
cache = {}
def lemma(w):
    if w in cache: return cache[w]
    try:
        res = an.lemmatize(w)
        cands = res[0][1] if res and res[0][1] else [w]
    except Exception:
        cands = [w]
    l = tr_lower(max(cands, key=len))
    l = {"sıvas":"sivas","genelmek":"genel","yunmak":"yunan","yermek":"yer","refetmek":"refet","kararmak":"karar","ortay":"orta","şeklî":"şekil","milliye":"millî","kazım":"kâzım","hakk":"hak"}.get(l, l)
    cache[w] = l
    return l

WORD = re.compile(r"[A-Za-zÇĞİÖŞÜçğıöşüÂâÎîÛû']+")
counts = collections.Counter()
surface = collections.defaultdict(collections.Counter)
examples = collections.defaultdict(list)
total = 0
for si, s in enumerate(sentences):
    seen = set()
    for tok in WORD.findall(s):
        base = tok.split("'")[0]
        if len(base) < 3: continue
        low = tr_lower(base)
        if low in STOP: continue
        l = lemma(low)
        if l in STOP or len(l) < 3: continue
        total += 1
        counts[l] += 1
        surface[l][low] += 1
        if l not in seen:
            seen.add(l); examples[l].append(si)

top = counts.most_common(200)
out = {"total_tokens": total, "sentences": len(sentences), "words": []}
import random
random.seed(1)
for w, c in top:
    idx = examples[w]
    pick = sorted(random.sample(idx, min(4, len(idx))))
    ex = [sentences[i][:260] for i in pick]
    out["words"].append({"w": w, "c": c, "forms": [f for f, _ in surface[w].most_common(4)], "ex": ex})
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
print(total, len(sentences))
for w, c in top[:60]: print(w, c, end=" | ")
