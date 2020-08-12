import lxml, sys
from lxml import etree

class MscxSerializer:
	def serialize(self, et, indent=0):
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
				self.serialize(element, indent + 1)
		if has_child:
			print ('\t'*(indent)) + '</%s>' % et.tag
		elif has_text:
			print '</%s>' % et.tag