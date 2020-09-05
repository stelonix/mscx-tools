import pyphen
pyphen.language_fallback('pt_BR')
dic = pyphen.Pyphen(lang='pt_BR')
txt = """ hino """
expl = txt.split()
for w in expl:
	print dic.inserted(w)