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

#subparsers = parser.add_subparsers(title = 'subcommands')

# parser_cat = subparsers.add_parser('cat')
# parser_cat.add_argument('src')
# parser_cat.add_argument('dst')
# parser_cat.add_argument('-s', '--skeleton')
# parser_cat.set_defaults(target=cat)

parser.add_argument('in_file', action="store")
group = parser.add_mutually_exclusive_group()
group.add_argument('--build-cache', '-b', action="store_true", dest="build_cache")
cache_group = parser.add_mutually_exclusive_group()
#cache_group.add_argument('--cache-src', '-s', action="store_true", dest="cache_src")
#parser.add_argument('--cache-src', required='--build_cache' in sys.argv, action="store", dest="cache_src")
group.add_argument('-a', action="store_true", dest="apply_cache")
group.add_argument('--cat', '-c', action="store_true", dest="opt_cat")
group.add_argument('--print-test', '-p', action="store_true", dest="print_test")
parser.add_argument('-o', action="store", dest="out_file")



opts = parser.parse_args()
in_file = get_real_path(opts.in_file)
out_file = get_real_path(opts.out_file) if opts.out_file != None else "outfile.mscx"

if os.path.isfile(out_file):
	overwrite = input('File already exists. Overwrite? [Y]es [N]o\n')
	if overwrite.lower() != 'y':
		sys.exit(0)

def load_target(target):
	return (target, deepcopy(target.xpath('/museScore/Score/Staff')[0]))

def load_targets(target_list):
	global other_songs
	root = etree.parse('/home/stel/Documents/MuseScore2/Scores/Justiceiro/Remake/Junho/' + file)
	other_songs.append(load_target(root))

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
	if atop == 'None':
		Chords[root]['None']
		if not pos[0] in Chords[root]['None']['x']:
			Chords[root]['None']['x'][pos[0]] = 0
		if not pos[1] in Chords[root]['None']['y']:
			Chords[root]['None']['y'][pos[1]] = 0
		Chords[root]['None']['x'][pos[0]] += 1
		Chords[root]['None']['y'][pos[1]] += 1
		return
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
			targ_pos = ('-0.5', '-1.5')
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

			try:
				if current_note == 'None':
					myt_x = Chords[targ_chord]['None']['x']
					myt_y = Chords[targ_chord]['None']['y']
				else:
					myt_x = Chords[targ_chord][current_note[0]][current_note[3]][current_note[2]]['x']
					myt_y = Chords[targ_chord][current_note[0]][current_note[3]][current_note[2]]['y']
				dec_list_x = {Decimal(key): value for (key,value) in myt_x.iteritems()}
				dec_list_y = {Decimal(key): value for (key,value) in myt_y.iteritems()}
				new_x = sorted(dec_list_x, key=dec_list_x.get, reverse=True)[0]
				new_y = sorted(dec_list_y, key=dec_list_y.get, reverse=True)[0]
			except:
				sys.stderr.write('error applying\n')
				new_x = -0.5
				new_y = -1.5
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
if opts.opt_cat:
	pass
elif opts.print_test:
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
	if os.path.isdir(in_file):
		for file in os.listdir(in_file):
			full_path = os.path.join(in_file, file)
			try:
				if os.path.isdir(full_path) or not file.endswith('.mscx'):
					continue
				else:
					xml_file = objectify.parse(full_path)
					h = xml_file.xpath('/museScore')[0]
					measures = h.Score.Staff.Measure

					for m in measures:
						extract_measure_data(m)
					old = os.dup(1)
					os.close(1)
					os.open(os.path.join(out_file, file), os.O_WRONLY|os.O_CREAT)

					print '<?xml version="1.0" encoding="UTF-8"?>'
					#current_score = etree.parse(in_file)
					serialize_xml(xml_file.getroot())
					os.close(1)
					os.dup(old)
					os.close(old)
			except:
				print "error in file %s" % (full_path)
	else:

		xml_file = objectify.parse(in_file)
		h = xml_file.xpath('/museScore')[0]
		#print h
		measures = h.Score.Staff.Measure
		for m in measures:
			extract_measure_data(m)
			#except:
			#	print "fail"
				#print pretty(Chords)
		print 'opening out_file = %s' % (out_file)
		old = os.dup(1)
		os.close(1)

		os.open(out_file, os.O_WRONLY|os.O_CREAT)

		print '<?xml version="1.0" encoding="UTF-8"?>'
		#current_score = etree.parse(in_file)
		serialize_xml(xml_file.getroot())
		os.close(1)
		os.dup(old)
		os.close(old)
		#with open(out_file, 'wb') as doc:
		#xml_file.write_c14n("TestPrimeiro.mscx")
			#xml_file.write(doc, xml_declaration=True, encoding='UTF-8')
			#doc.write(etree.tostring(xml_file, pretty_print = True))
		sys.exit(0)
print in_file, out_file

#print pretty(Chords)

sys.exit(0)
