import lxml
from lxml import etree
from copy import deepcopy

def get_targ_list(filename="targs.txt"):
	fo = open(filename, "r+")
	lines = fo.readlines()
	fo.close()
	for x in range(len(lines)):
		lines[x] = lines[x].strip()
	return lines

def load_targets(target_list):
	global other_songs
	root = etree.parse('/home/stel/Documents/MuseScore2/Scores/Justiceiro/Remake/Junho/' + file)
	other_songs.append(deepcopy(root.xpath('/museScore/Score/Staff')[0]))

def get_last_measure(targ_file):
	return targ_file.xpath('/Staff/Measure')[-1]

def get_last_measure_index(targ_file):
	return targ_file.xpath('/museScore/Score/Staff')[0].index(targ_file.xpath('/museScore/Score/Staff/Measure')[-1])

def remove_lbreaks(measure):
	for bad in measure.xpath("/LayoutBreak"):
		bad.getparent().remove(bad)

def ends_with_hbox(measure):
	return not len(last_measure.xpath('/HBox')) == 0

lbs = ["""<LayoutBreak>
          <subtype>line</subtype>
          </LayoutBreak>""",
		  """<LayoutBreak>
          <subtype>section</subtype>
          </LayoutBreak>"""]

keysig = ["""<Clef>
          <concertClefType>G</concertClefType>
          <transposingClefType>G</transposingClefType>
          </Clef>""",
        """<KeySig>
          <accidental>0</accidental>
          </KeySig>"""]
def add_lbreaks(measure):
	global lbs
	measure.insert(2, etree.fromstring(lbs[0]))
	measure.insert(2, etree.fromstring(lbs[1]))

def get_vbox(score):
	return score[cur_index].xpath('/Staff/VBox')[0]

def get_measures(score):
	return score.xpath('/Staff/Measure')

def has_keysing(score):
	ms = get_measures(score)
	return len(ms[0].xpath('/KeySig')) > 0

def add_c_keysig(score):
	ms = get_measures(score)
	ms[0].insert(2, etree.fromstring(keysig[1]))
	ms[0].insert(2, etree.fromstring(keysig[0]))

other_songs = []
lines = get_targ_list()
load_targets(lines)
targ_file = etree.parse(r'/home/stel/Documents/MuseScore2/Scores/Justiceiro/Remake/Junho/01_C.mscx')
left_over = len(lines)
i = 0
init_l = left_over
while left_over > 0:
	print "lines[:10]: ", lines[:10]
	for file in lines[:10]:
		print "insert %s into %s" % (file, "Result%d"%i)
		cur_index = len(other_songs) - 1
		last_measure = get_last_measure(other_songs[cur_index])
		#if not len(last_measure.xpath('/LayoutBreak')) == 0:
		#	for bad in last_measure.xpath("/LayoutBreak"):
	  	#		bad.getparent().remove(bad)
		remove_lbreaks(last_measure)
		targ = last_measure
		if ends_with_hbox(targ):
			targ = last_measure.xpath('/HBox')
		add_lbreaks(targ)
		vbox = get_vbox(other_songs[cur_index])
		list_of_to_copy = get_measures(other_songs[cur_index])
		last_measure_index = get_last_measure_index(targ_file)
		#nextm = int(  targ_file.xpath('/museScore/Score/Staff')[0].index(targ_file.xpath('/museScore/Score/Staff/Measure')[-1]["number"])+1
		#nextm = int(targ_file.xpath('/museScore/Score/Staff/Measure')[-1]["number"])
		targ_file.xpath('/museScore/Score/Staff')[0].insert(last_measure_index, vbox)
		#last_measure_index += 1
		for measure in list_of_to_copy:
			last_measure_index = get_last_measure_index(targ_file)
			#measure["number"] = str(nextm)
			#targ_file.xpath('/museScore/Score/Staff')[0]
			targ_file.xpath('/museScore/Score/Staff')[0].insert(last_measure_index, measure)

		#measures = targ_file.xpath('/museScore/Score/Staff/Measure')

		#left_over -= len(deepcopy(lines)[len(lines[:10]):][:10])
		#with open("Result%d.mscx"%i, 'wb') as doc:
			doc.write(etree.tostring(targ_file, pretty_print = True))
	i += 1
	if len(lines) > 0:
		print len(lines)
		del lines[0:10]
		print "after pop: %d" %  len(lines)
		cur_file = '/home/stel/Documents/MuseScore2/Scores/Justiceiro/Remake/Junho/'+lines.pop(0)
		print "current file: " + cur_file
		targ_file = etree.parse(cur_file)
	print left_over
#for m in measures:
	#print etree.tostring(m)

print "total: ", len(measures)

#with open("Result.mscx", 'wb') as doc:
#   doc.write(etree.tostring(targ_file, pretty_print = True))
	#targ_file.xpath('/museScore/Score/Staff')[0].insert(last_measure_index + 1, other_songs[cur_index])
#	print etree.tostring(targ_file.xpath('/museScore/Score/Staff/S')[0])
	#print
	#print etree.tostring(last_measure)
	#etree.fromstring(lbs)
	#print etree.tostring(other_songs[cur_index])
