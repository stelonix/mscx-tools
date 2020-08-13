import Score, MscxSerializer, Util
import lxml
from lxml import etree, objectify
from Score import Score

mscx = MscxSerializer.MscxSerializer()
other_songs = Util.load_targets(Util.get_targ_list())

targ_file = other_songs.pop(0)

hs = targ_file.tree.findall('.//Harmony')
for h in hs:
	ht = objectify.fromstring(etree.tostring(h))
	try:
		tname = ht.name
	except:
		tname = ''
	try:
		tbase = int(ht.base)
	except:
		tbase = None
	#print ht.root
	print Util.harmony_to_chord(int(ht.root), tname, ht.base)
sys.exit(0)
for score in other_songs:
	targ_file.join_score(score)
print '<?xml version="1.0" encoding="UTF-8"?>'
mscx.serialize(targ_file.tree.getroot())
