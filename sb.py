import lxml, sys, pdb
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
	for file in target_list:
		root = etree.parse('/home/stel/Documents/MuseScore2/Scores/ICEFLU/Alex/newer/fixed/' + file)
		other_songs.append(deepcopy(root.xpath('/museScore/Score/Staff')[0]))

def get_last_measure(targ_file):
	#pdb.set_trace()
	return targ_file.xpath('/Staff/Measure')[-1]

def get_last_measure_index(targ_file):
	return targ_file.xpath('/museScore/Score/Staff')[0].index(targ_file.xpath('/museScore/Score/Staff/Measure')[-1])

def remove_lbreaks(measure):
	#if not len(last_measure.xpath('/LayoutBreak')) == 0:
	for bad in measure.xpath("/LayoutBreak"):
		pdb.set_trace()
		bad.getparent().remove(bad)

def ends_with_hbox(measure):
	return not len(measure.xpath('/HBox')) == 0

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

timesig44 = ["""<TimeSig>
          <visible>0</visible>
          <sigN>4</sigN>
          <sigD>4</sigD>
          <showCourtesySig>0</showCourtesySig>
          </TimeSig>""",
        """<Segment>
          <leadingSpace>-0.5</leadingSpace>
          <trailingSpace>-1.9</trailingSpace>
          </Segment>"""]

last_timesig = '44'
def add_lbreaks(measure):
	global lbs
	measure.insert(2, etree.fromstring(lbs[0]))
	measure.insert(2, etree.fromstring(lbs[1]))

def get_vbox(score):
	return score.xpath('/Staff/VBox')[0]

def get_measures(score):
	return score.xpath('/Staff/Measure')

def has_keysig(score):
	#pdb.set_trace()
	ms = get_measures(score)
	return len(ms[0].xpath('KeySig')) > 0

def has_timesig(score):
	ms = get_measures(score)
	return len(ms[0].xpath('TimeSig')) > 0

def add_c_keysig(score):
	ms = get_measures(score)
	ms[0].insert(2, etree.fromstring(keysig[1]))
	ms[0].insert(2, etree.fromstring(keysig[0]))

def add_44_timesig(score):
	ms = get_measures(score)
	ms[0].insert(2, etree.fromstring(timesig44[1]))
	ms[0].insert(2, etree.fromstring(timesig44[0]))

def normalize_first_measure(score):
	#pdb.set_trace()
	global last_timesig
	if not has_keysig(score):
		add_c_keysig(score)
	if not has_timesig(score):
	#	cur_timesig = get_measures(score)[0].xpath('TimeSig')[0]
	#	if cur_timesig == None
	#	cur_timesig = stringify_timesig()
	#	if cur_timesig != last_timesig:
	#	last_timesig = cur_timesig
		add_44_timesig(score)

def normalize_last_measure(targ_score):
	last_measure = get_last_measure(targ_score)
	#pdb.set_trace()
	remove_lbreaks(last_measure)
	targ = last_measure
	if ends_with_hbox(targ):
		targ = last_measure.xpath('/HBox')
	add_lbreaks(targ)

def stringify_timesig(timesig):
	return timesig.xpath('sigN').text + timesig.xpath('sigD').text
other_songs = []
lines = get_targ_list()
load_targets(lines)
targ_file = etree.parse(r'/home/stel/Documents/MuseScore2/Scores/ICEFLU/Alex/newer/fixed/I_C.mscx')

num_measures = len(get_measures(other_songs[0]))+1

def serialize_xml(et, indent=0):
	#create new tag
	sys.stdout.write(('\t'*indent).encode('utf-8'))
	#print 'lol'
	new_tag = etree.fromstring('<%s/>' % et.tag)
	for a in et.attrib.keys():
		new_tag.attrib[a] = et.attrib[a]
	new_tag = etree.tostring(new_tag)
	num_child = len(et.getchildren())

	autoclose_tag = et.text == None
	has_text = len(et.text) > 0 if not autoclose_tag else False
	has_child = num_child > 0

	if num_child > 0 or (has_text or (not autoclose_tag and not has_child)):
		new_tag = new_tag[:len(new_tag) - 2] + '>'
	else:
		new_tag = new_tag[:len(new_tag) - 2] + '/>'

	if (not has_child) and has_text:
		#print '%s not has_child and has_text indent: %d' % (et.tag, indent)
		sys.stdout.write(new_tag.encode('utf-8'))
	else:
		#print '%s has_child and has_text indent: %d' % (et.tag, indent)
		print new_tag

	if not autoclose_tag and len(et.text.strip()) > 0:
		sys.stdout.write(et.text.encode('utf-8'))
	for element in et.iterchildren():
		if element.tag == 'text':
			print ('\t'*(indent + 1)) + etree.tostring(element).strip()
		else:
			serialize_xml(element, indent + 1)
	if has_child:
		print ('\t'*(indent)) + '</%s>' % et.tag
	elif has_text:
		print '</%s>' % et.tag
for cur_index in xrange(0, len(lines)):
	cur_score = other_songs[cur_index]
	normalize_last_measure(cur_score)

	vbox = get_vbox(cur_score)
	list_of_to_copy = get_measures(cur_score)
	#print list_of_to_copy
	#sys.exit(0)
	last_measure_index = get_last_measure_index(targ_file)

	normalize_first_measure(cur_score)

	targ_file.xpath('/museScore/Score/Staff')[0].insert(last_measure_index+1, vbox)
	#targ_file.xpath('/museScore/Score/Staff')[0].insert(last_measure_index, vbox)
	last_measure_index += 1
	for measure in list_of_to_copy:

		#measure["number"] = str(nextm)
		#targ_file.xpath('/museScore/Score/Staff')[0]
		measure.attrib['number'] = str(num_measures)
		targ_file.xpath('/museScore/Score/Staff')[0].insert(last_measure_index+1, measure)
		last_measure_index = get_last_measure_index(targ_file)
		num_measures += 1

	#measures = targ_file.xpath('/museScore/Score/Staff/Measure')

	#left_over -= len(deepcopy(lines)[len(lines[:10]):][:10])
	#if cur_index == 8:
	#	break
#with open("ResultGlauco.mscx", 'wb') as doc:
#	doc.write(etree.tostring(targ_file, pretty_print = True,xml_declaration=True,))
print '<?xml version="1.0" encoding="UTF-8"?>'
serialize_xml(targ_file.getroot())
sys.exit(0)
#print "algo"
#for m in measures:
	#print etree.tostring(m)
