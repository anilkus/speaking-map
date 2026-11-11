"""freq.json -> freq2.json: ilk 180 kelimeye elle kategori atar."""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
K = set("paşa bey rauf kemal ali ismet mustafa kâzım refet cemal ethem tevfik nurettin efendi hazretleri padişah halife arkadaş vali reis vekil mebus delege kumandan zevat memur".split())
Y = set("istanbul ankara sivas erzurum anadolu izmir türkiye doğu yunan ingiliz osmanlı itilâf türk vilâyet havali mıntıka vatan memleket".split())
U = set("meclis heyet hükümet devlet ordu fırka cemiyet kongre kolordu kabine teşkilât cumhuriyet hilâfet harbiye konferans riyaset makam kuvayi".split())
drop = {"nutuk", "top", "konu", "yerinmek"}
d["words"] = [w for w in d["words"] if w["w"] not in drop][:180]
for w in d["words"]:
    x = w["w"]
    w["k"] = "kisi" if x in K else "yer" if x in Y else "kurum" if x in U else "kavram"
json.dump(d, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False)
