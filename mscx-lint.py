import lxml
from lxml import etree
from lxml import objectify
from copy import deepcopy
import argparse, sys, os, pickle
from decimal import Decimal
import operator

cwd = os.getcwd()
other_songs = []
def get_real_path(p):
	global cwd
	tmp = p
	if p != '/':
		tmp = os.path.join(cwd, tmp)
	return os.path.abspath(tmp)


parser = argparse.ArgumentParser(description='Process some integers.')

parser.add_argument('in_file', action="store")
group = parser.add_mutually_exclusive_group()
group.add_argument('--build-cache', '-b', action="store_true", dest="build_cache")
group.add_argument('-a', action="store_true", dest="apply_cache")
group.add_argument('--print-test', '-p', action="store_true", dest="print_test")
parser.add_argument('-o', action="store", dest="out_file")



opts = parser.parse_args()
in_file = get_real_path(opts.in_file)
out_file = get_real_path(opts.out_file) if opts.out_file != None else "outfile.mscx"



def get_targ_list(filename="targs.txt"):
	fo = open(filename, "r+")
	lines = fo.readlines()
	fo.close()
	for x in range(len(lines)):
		lines[x] = lines[x].strip()
	return lines

def load_target(target):
	return (target, deepcopy(target.xpath('/museScore/Score/Staff')[0]))

def load_targets(target_list):
	global other_songs
	root = etree.parse('/home/stel/Documents/MuseScore2/Scores/Justiceiro/Remake/Junho/' + file)
	other_songs.append(load_target(root))

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

def can_has_beam(chord):
	#dt = chord.xpath("/durationType").text()
	dt = chord
	return dt != "quarter" and dt != "half" and dt != "whole"

def extract_note(child, last_dir):
	stem_direction = last_dir
	has_beam = False
	if hasattr(child, 'BeamMode'):
		if child.BeamMode.text != 'no':
			has_beam = True
	if hasattr(child, 'Beam'):
		has_beam = True
	if not can_has_beam(child.durationType):
		has_beam = False
	if hasattr(child, 'StemDirection'):
		stem_direction = child.StemDirection.text
	#prev_chord_duration = child.durationType
	return (child.Note.pitch, child.durationType, has_beam, stem_direction)

Chords = {}
def add_chord_stat(root, atop, stem_dir, has_beam,pos):
	global Chords
	if not root in Chords:
		Chords[root] = {}
	if not atop in Chords[root]:
		Chords[root][atop] = {}
	if not stem_dir in Chords[root][atop]:
		Chords[root][atop][stem_dir] = {}
	if not has_beam in Chords[root][atop][stem_dir]:
		Chords[root][atop][stem_dir][has_beam] = {}
	if not 'x' in Chords[root][atop][stem_dir][has_beam]:
		Chords[root][atop][stem_dir][has_beam]['x'] = {}
	if not 'y' in Chords[root][atop][stem_dir][has_beam]:
		Chords[root][atop][stem_dir][has_beam]['y'] = {}
	if not pos[0] in Chords[root][atop][stem_dir][has_beam]['x']:
		Chords[root][atop][stem_dir][has_beam]['x'][pos[0]] = 0
	if not pos[1] in Chords[root][atop][stem_dir][has_beam]['y']:
		Chords[root][atop][stem_dir][has_beam]['y'][pos[1]] = 0
	Chords[root][atop][stem_dir][has_beam]['x'][pos[0]] += 1
	Chords[root][atop][stem_dir][has_beam]['y'][pos[1]] += 1
#Chords[root][atop_note][with_stem][is_beamed][x] = {x_pos: number_of_uses}
def pretty(value, htchar='\t', lfchar='\n', indent=0):
    nlch = lfchar + htchar * (indent + 1)
    if type(value) is dict:
        items = [
            nlch + repr(key) + ': ' + pretty(value[key], htchar, lfchar, indent + 1)
            for key in value
        ]
        return '{%s}' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is list:
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '[%s]' % (','.join(items) + lfchar + htchar * indent)
    elif type(value) is tuple:
        items = [
            nlch + pretty(item, htchar, lfchar, indent + 1)
            for item in value
        ]
        return '(%s)' % (','.join(items) + lfchar + htchar * indent)
    else:
        return repr(value)

def extract_measure_data(m):
	stem_direction = "down"
	current_note = None
	in_a_tick = False
	for child in m.iterchildren():
		if child.tag == "Beam":
			try:
				stem_direction = child.StemDirection.text
			except:
				pass
		elif child.tag == "Chord":
			current_note = extract_note(child, stem_direction)
			stem_direction = current_note[3]
		elif child.tag == "Harmony":
			targ_chord = child.root.text
			if hasattr(child, 'name'):
				targ_chord += ':' + child.name.text
			targ_pos = ('0.0', '-2.5')
			if hasattr(child, 'pos'):
				targ_pos = (child.pos.attrib['x'], child.pos.attrib['y'])
			if in_a_tick:
				current_note = "None"
			else:
				for s in child.itersiblings():
					if s.tag == "Chord":
						current_note = extract_note(s, stem_direction)
						break
			print "Chords[%s][%s][%s][%s][%s] = " % (targ_chord, current_note[0], current_note[3], current_note[2], targ_pos[1])
			#l_dec = sorted(Decimal(c) for c in Chords[targ_chord][current_note[0]][current_note[3]][current_note[2]])
			myt_x = Chords[targ_chord][current_note[0]][current_note[3]][current_note[2]]['x']
			myt_y = Chords[targ_chord][current_note[0]][current_note[3]][current_note[2]]['y']
			dec_list_x = {Decimal(key): value for (key,value) in myt_x.iteritems()}
			dec_list_y = {Decimal(key): value for (key,value) in myt_y.iteritems()}
			#print myt
			#print dec_list
			new_x = sorted(dec_list_x, key=dec_list_x.get, reverse=True)[0]
			new_y = sorted(dec_list_y, key=dec_list_y.get, reverse=True)[0]
			if hasattr(child, 'pos'):
				child.pos.attrib['x'] = str(new_x)
				child.pos.attrib['y'] = str(new_y)
			else:
				child.append(etree.fromstring('<pos x="%s" y="%s"/>'%(str(new_x), str(new_y))))
			#print sorted(dec_list, key=operator.itemgetter(1))
			#(child.Note.pitch, child.durationType, has_beam, stem_direction)
		elif child.tag == "tick":
			in_a_tick = True

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
	#if et.tail != None and len(et.tail.strip()) > 0:
	#	print et.tail
if opts.print_test:
	print '<?xml version="1.0" encoding="UTF-8"?>'
	current_score = etree.parse(in_file)
	serialize_xml(current_score.getroot())
	sys.exit(0)
elif opts.build_cache:
	files_to_stat = []
	usage_cache = {}
	in_dir = in_file
	print 'building'
	for file in os.listdir(in_dir):
		all_notes = []
		if file.endswith(".mscx"):
			beams = {}
			current_beam = None

			prev_chord_duration = None
			has_beam = False

			actual_file = os.path.join(in_dir, file)
			current_score = load_target(etree.parse(actual_file))
			obj_score = objectify.fromstring(etree.tostring(current_score[0]))
			measures = obj_score.Score.Staff.Measure


			for m in measures:
				stem_direction = "down"
				current_note = None
				in_a_tick = False
				for child in m.iterchildren():
					if child.tag == "Beam":
						try:
							stem_direction = child.StemDirection.text
						except:
							print 'fail'
							pass
					elif child.tag == "Chord":
						current_note = extract_note(child, stem_direction)
						stem_direction = current_note[3]
						all_notes.append(current_note)
					elif child.tag == "Harmony":
						targ_chord = child.root.text
						if hasattr(child, 'name'):
							targ_chord += ':' + child.name.text
						targ_pos = ('0.0', '-2.5')
						if hasattr(child, 'pos'):
							targ_pos = (child.pos.attrib['x'], child.pos.attrib['y'])
						if in_a_tick:
							current_note = "None"
						else:
							for s in child.itersiblings():
								if s.tag == "Chord":
									current_note = extract_note(s, stem_direction)
									break
						#print "H: " + targ_chord + " (%s, %s)" % targ_pos + " on note " + str(current_note)
						#print "Chords[%s][%s][%s][%s][%s] = +1" % (targ_chord, current_note[0], current_note[3], current_note[2], targ_pos[1])
						add_chord_stat(targ_chord, current_note[0], current_note[3], current_note[2], targ_pos)
						#(child.Note.pitch, child.durationType, has_beam, stem_direction)
					elif child.tag == "tick":
						in_a_tick = True

			#for note in all_notes:
			#	print note
			# @@ !! IMPORTANT  !! @@
			#Chords[root][atop_note][with_stem][is_beamed][x] = {x_pos: number_of_uses}
	print pretty(Chords)
	pickle.dump( Chords, open( "db.pickle", "wb" ) )
elif opts.apply_cache:
	Chords = pickle.load( open( "db.pickle", "rb" ))
	xml_file = objectify.parse(in_file)
	h = xml_file.xpath('/museScore')[0]
	#print h
	measures = h.Score.Staff.Measure
	for m in measures:
		extract_measure_data(m)
		#except:
		#	print "fail"
			#print pretty(Chords)
	print 'saving'
	new_tostring = etree.tostring(xml_file,pretty_print=True,xml_declaration=True, encoding='UTF-8')
	#after_pretty = objectify.fromstring(new_tostring)
	#print after_pretty[0].getroot()
	after_pretty = etree.fromstring(new_tostring)
	h = after_pretty.xpath('/museScore')[0]
	lines_to_correct = []
	final_lines = []
	for text in h.xpath('Score/Staff/VBox/Text'):
		#print etree.tostring(text.xpath('text')[0])
		#init_src = text.text.sourceline

		#lfdsf
		print etree.tostring(text.xpath('text')[0]).replace('\n','')
		# endline_num = init_src + (len(etree.tostring(text.text).strip().split()) - 1)
		# if text.Style.text == "Title":
		# 	lines_to_correct[0] = (init_src, endline_num)
		# 	final_lines[0] = etree.tostring(text.xpath('text')[0])
		# elif text.Style.text == "Subtitle":
		# 	lines_to_correct[1] = (init_src, endline_num)
		# 	final_lines[1] = etree.tostring(text.xpath('text')[0])
	#splitted = new_tostring.split('\n')

	#for i in xrange(endline_num-init_src):

	#for line in xrange(len(splitted)):

	print init_src, endline_num
	sys.exit(0)
	with open("TestPrimeiro.mscx", 'wb') as doc:
	#xml_file.write_c14n("TestPrimeiro.mscx")
		#xml_file.write(doc, xml_declaration=True, encoding='UTF-8')
		doc.write(etree.tostring(xml_file, pretty_print = True))
	sys.exit(0)
print in_file, out_file

#print pretty(Chords)

sys.exit(0)
