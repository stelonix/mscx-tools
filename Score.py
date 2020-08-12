import lxml, sys, pdb, Util
from lxml import etree
from copy import deepcopy

def solve_spans(measures, from_id):
	spanner_ids = from_id
	spans = []
	end_spans = []
	slurs = []
	for m in measures:
		spans += m.findall('.//Tie') + m.findall('.//Volta') + m.findall('.//Glissando')
		slurs += m.findall('.//Slur')
		end_spans += m.findall('.//endSpanner')
	shared_ids = sorted(spans + slurs, key=lambda elem: int(elem.attrib['id']))
	for span in shared_ids:
		if span.tag == 'Slur':
			span.attrib['id'] = str(spanner_ids)
			spanner_ids += 1
		else:
			span_id = span.attrib['id']
			for end_span in end_spans:
				if end_span.attrib['id'] == span_id:
					#sys.stderr.write('matched spans\n')
					end_span.attrib['id'] = str(spanner_ids)
					span.attrib['id'] = str(spanner_ids)
					spanner_ids += 1
	return spanner_ids

class Score:
	def __init__(self, targ_file=None):
		if targ_file != None:
			self.load_score(targ_file)
			self.highest_id = 2
			self.calc_spans()
			self.measure_number = len(self.tree.xpath('/museScore/Score/Staff/Measure'))+1
			self.filename = targ_file

	def get_staff(self):
		pass

	def join_score(self, score):
		list_of_to_copy = score.tree.xpath('/museScore/Score/Staff')[0].getchildren()
		sys.stderr.write('\x1B[1;1m[SPANS]\x1B[1;0m ' + score.filename + '\n')
		self.calc_spans(list_of_to_copy)
		score.normalize_first_measure()
		for el in reversed(list_of_to_copy):
			if el.tag == 'Measure' or el.tag == 'HBox':
				Util.add_lbreaks(el)
				break
		for el in list_of_to_copy:
			c = deepcopy(el)
			if c.tag == 'Measure':
				c.attrib['number'] = str(self.measure_number)
				self.measure_number += 1
			self.tree.xpath('/museScore/Score/Staff')[0].append(c)

	def append_measure(self, measures):
		measures.getchildren()

	def calc_spans(self, new_data=None):
		if new_data == None:
			new_data = self.get_measures()
		self.highest_id = solve_spans(new_data, self.highest_id)

	def load_score(self, targ_file):
		self.tree = etree.parse(targ_file)
	
	def get_last_measure(self):
		#pdb.set_trace()
		return self.tree.xpath('/museScore/Score/Staff/Measure')[-1]

	def get_vbox(self):
		return self.tree.xpath('/museScore/Score/Staff/VBox')[0]

	def get_measures(self):
		return self.tree.xpath('/museScore/Score/Staff/Measure')

	def has_keysig(self):
		#pdb.set_trace()
		ms = self.get_measures()
		return len(ms[0].xpath('KeySig')) > 0

	def has_timesig(self):
		ms = self.get_measures()
		return len(ms[0].xpath('TimeSig')) > 0
	
	def normalize_first_measure(self):
		#pdb.set_trace()
		ms = self.get_measures()
		global added_cks
		if not self.has_keysig() and not added_cks:
			Util.add_c_keysig(ms[0])
			added_cks = True
		else:
			added_cks = False
		if not self.has_timesig():
			Util.add_44_timesig(ms[0])
	
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