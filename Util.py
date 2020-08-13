# encoding: utf-8
import lxml, Score
from lxml import etree

lbs = ["""<LayoutBreak>
          <subtype>line</subtype>
          # </LayoutBreak>"""]
		  # """<LayoutBreak>
          # <subtype>section</subtype>
          # </LayoutBreak>"""]

keysig = ["""<Clef>
          <concertClefType>G</concertClefType>
          <transposingClefType>G</transposingClefType>
          </Clef>""",
        """<KeySig>
          <accidental>0</accidental><visible>0</visible>
          </KeySig>""",
		"""<Segment>
          <leadingSpace>0</leadingSpace>
          <trailingSpace>-0.6</trailingSpace>
          </Segment>"""]

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
keysig = ["""<Clef>
          <concertClefType>G</concertClefType>
          <transposingClefType>G</transposingClefType>
          </Clef>""",
        """<KeySig>
          <accidental>0</accidental><visible>0</visible>
          </KeySig>""",
          """<Segment>
          <leadingSpace>0</leadingSpace>
          <trailingSpace>-0.6</trailingSpace>
          </Segment>"""]

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

def add_lbreaks(element):
     element.insert(2, etree.fromstring(lbs[0]))

def add_c_keysig(measure):
     measure.insert(2, etree.fromstring(keysig[2]))
     measure.insert(2, etree.fromstring(keysig[1]))
     measure.insert(2, etree.fromstring(keysig[0]))

def add_44_timesig(measure):
     measure.insert(2, etree.fromstring(timesig44[1]))
     measure.insert(2, etree.fromstring(timesig44[0]))

def get_targ_list(filename="targs.txt"):
     fo = open(filename, "r+")
     lines = fo.readlines()
     fo.close()
     for x in range(len(lines)):
          lines[x] = lines[x].strip()
     return lines

def load_targets(target_list):
     join_targets = []
     for file in target_list:
          join_targets.append(Score.Score(file))
     return join_targets


#'@♭♭', '@♭',   '@',    '@♯',   '@♯♯',
#'F♭♭', 'F♭',   'F',    '@♯',   '@♯♯',
#'@♭♭', '@♭',   '@',    '@♯',   '@♯♯',
#'@♭♭', '@♭',   '@',    '@♯',   '@♯♯',
spellings = [
        'F♭♭', 'C♭♭',  'G♭♭', 'D♭♭', 'A♭♭', 'E♭♭', 'B♭♭',  'F♭', 
        'C♭',   'G♭',  'D♭' , 'A♭',  'E♭',  'B♭',  'F', 
        'C',    'G',   'D' ,  'A',   'E',   'B',  'F♯', 
        'C♯',   'G♯',  'D♯' , 'A♯',  'E♯',  'B♯', 'F♯♯',
        'C♯♯',   'G♯♯',  'D♯♯' , 'A♯♯',  'E♯♯',  'B♯♯'
    ]

def harmony_to_chord(harmony, name, base=None):
     if base != None:
          name = name + '/' + spellings[base+1]
     return spellings[harmony+1] + str(name)