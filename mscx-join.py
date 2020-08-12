import Score, MscxSerializer
import lxml
from lxml import etree
from Score import Score

def get_targ_list(filename="targs.txt"):
	fo = open(filename, "r+")
	lines = fo.readlines()
	fo.close()
	for x in range(len(lines)):
		lines[x] = lines[x].strip()
	return lines

def load_targets(target_list):
	global other_songs
	for file in target_list:
		other_songs.append(Score(file))

mscx = MscxSerializer.MscxSerializer()
other_songs = []
lines = get_targ_list()
load_targets(lines)
targ_file = Score(r'/mnt/c/Users/maria/mscx-tools/scores/md/04_Gm.mscx')
num_measures = len(targ_file.tree.xpath('/museScore/Score/Staff/Measure'))+1

for score in other_songs:
	targ_file.join_score(score)
print '<?xml version="1.0" encoding="UTF-8"?>'
mscx.serialize(targ_file.tree.getroot())
#print len(tmp)
#sys.exit(1)