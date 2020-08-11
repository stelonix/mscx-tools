def get_targ_list(filename="targs.txt"):
	fo = open(filename, "r+")
	lines = fo.readlines()
	fo.close()
	for x in range(len(lines)):
		lines[x] = lines[x].strip()
	return lines

class Score:
	def __init__(self, targ_file):
		pass

	def get_last_measure(targ_file):
	#pdb.set_trace()
	return targ_file.xpath('/Staff/Measure')[-1]

	def get_last_measure_index(targ_file):
		return targ_file.xpath('/museScore/Score/Staff')[0].index(targ_file.xpath('/museScore/Score/Staff/Measure')[-1])

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
		ms[0].insert(2, etree.fromstring(keysig[2]))
		ms[0].insert(2, etree.fromstring(keysig[1]))
		ms[0].insert(2, etree.fromstring(keysig[0]))

	def add_44_timesig(score):
		ms = get_measures(score)
		ms[0].insert(2, etree.fromstring(timesig44[1]))
		ms[0].insert(2, etree.fromstring(timesig44[0]))
	def normalize_first_measure(score):
		#pdb.set_trace()
		global last_timesig, added_cks
		if not has_keysig(score) and not added_cks:
			add_c_keysig(score)
			added_cks = True
		else:
			added_cks = False
		if not has_timesig(score):
			add_44_timesig(score)
	
class Measure:
	def __init__(self):
		pass
	def remove_lbreaks(self, measure):
		#if not len(last_measure.xpath('/LayoutBreak')) == 0:
		for bad in measure.xpath("/LayoutBreak"):
			pdb.set_trace()
			bad.getparent().remove(bad)

	def ends_with_hbox(self, measure):
		return not len(measure.xpath('/HBox')) == 0