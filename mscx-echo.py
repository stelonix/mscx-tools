import Score, MscxSerializer, Util
import lxml, sys
from lxml import etree, objectify
from copy import deepcopy
from Score import Score

mscx = MscxSerializer.MscxSerializer()

targ_file = Score(sys.argv[1])
in_file = deepcopy(targ_file)
in_file.added_cks = True
Util.add_lbreaks(targ_file.get_last_measure())
for i in xrange(1, int(sys.argv[2])):
	modi = deepcopy(in_file)
	for vb in modi.tree.xpath('//VBox'):
		vb.getparent().remove(vb)
	targ_file.join_score(modi, False)
print '<?xml version="1.0" encoding="UTF-8"?>'
mscx.serialize(targ_file.tree.getroot())
