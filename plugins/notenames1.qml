//=============================================================================
//  MuseScore
//  Music Composition & Notation
//
//  Note Names Plugin
//
//  Copyright (C) 2012 Werner Schweer
//  Copyright (C) 2013 - 2017 Joachim Schmitz
//  Copyright (C) 2014 Jörn Eichler
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License version 2
//  as published by the Free Software Foundation and appearing in
//  the file LICENCE.GPL
//=============================================================================

import QtQuick 2.0
import MuseScore 1.0

MuseScore {
	version: "2.0"
	description: qsTr("This plugin names notes as per your language setting")
	menuPath: "Plugins.Notes." + qsTr("Note Names") // this does not work, why?

	function nameChord (notes, text) {
                  var NOTE_COLOR = {
            'C': "#ff0000",
            'C♯': "#df7500",
            'D♭': "#df7500",
            'D': "#bfaf3f",
            'D♯': "#928f28",
            'E♭': "#928f28",
            'E': "#3A9D23",
            'F♭': "#3A9D23",
            'F': "#ae4b00",
            'F♯': "#348a1e",
            'G♭': "#348a1e",
            'G': "#22427c",
            'G♯': "#564966",
            'A♭': "#564966",
            'A': "#337ec9",
            'A♯': "#418686",
            'B♭': "#418686",
            'B': "#000000",
            'C♭': "#000000"
            };
                  var NOTE_HIGHER = {
            'C': "Ĉ",
            'C♯': "Ĉ♯",//Ƈ
            'D': "°Ɗ",
            'D♯': "Ɗ♯",//Ɗ
            'E♭': "Ȇ♭",
            'E': "Ȇ",
            'F': "Ḟ",
            'F♯': "Ḟ♯",//𑄨
            'G♭': "Ĝb",//Ģ
            'G': "Ĝ",
            'G♯': "Ĝ♯",
            'A♭': "Ȃ♭",
            'A': "Ȃ",
            'A♯': "Ȃ♯",
            'B♭': "Ɓb", //ℬ
            'B': "Ɓ"
            };
                  var NOTE_LOWER = {
            'C': "Č",
            'C♯': "Č♯",//Ƈ
            'D': "Ḑ",
            'D♯': "Ḑ♯",
            'E♭': "Ĕ♭",
            'E': "Ĕ",
            'F': "Ƒ",
            'F♯': "Ƒ♯",//𑄨
            'G♭': "Ģb",//
            'G': "Ģ",
            'G♯': "Ģ♯",
            'A♭': "Ȃ♭",
            'A': "Ȃ",
            'A♯': "Ȃ♯",
            'B♭': "Ɓb", //ℬ
            'B': "Ɓ"
            };
		for (var i = 0; i < notes.length; i++) {
			var targ_text = "";
			var sep = ","; // change to "\n" if you want them vertically
			if ( i > 0 )
				text.text = sep + text.text; // any but top note

			if (typeof notes[i].tpc === "undefined") // like for grace notes ?!?
				return
			switch (notes[i].tpc) {
				case -1: targ_text = "F♭♭"; break;
				case 0: targ_text = "C♭♭"; break;
				case 1: targ_text = "G♭♭"; break;
				case 2: targ_text = "D♭♭"; break;
				case 3: targ_text = "A♭♭"; break;
				case 4: targ_text = "E♭♭"; break;
				case 5: targ_text = "B♭♭"; break;
				case 6: targ_text = "F♭"; break;
				case 7: targ_text = "C♭"; break;

				case 8: targ_text = "G♭"; break;
				case 9: targ_text = "D♭"; break;
				case 10: targ_text = "A♭"; break;
				case 11: targ_text = "E♭"; break;
				case 12: targ_text = "B♭"; break;
				case 13: targ_text = "F"; break;
				case 14: targ_text = "C"; break;
				case 15: targ_text = "G"; break;
				case 16: targ_text = "D"; break;
				case 17: targ_text = "A"; break;
				case 18: targ_text = "E"; break;
				case 19: targ_text = "B"; break;

				case 20: targ_text = "F♯"; break;
				case 21: targ_text = "C♯"; break;
				case 22: targ_text = "G♯"; break;
				case 23: targ_text = "D♯"; break;
				case 24: targ_text = "A♯"; break;
				case 25: targ_text = "E♯"; break;
				case 26: targ_text = "B♯"; break;
				case 27: targ_text = "F♯♯"; break;
				case 28: targ_text = "C♯♯"; break;
				case 29: targ_text = "G♯♯"; break;
				case 30: targ_text = "D♯♯"; break;
				case 31: targ_text = "A♯♯"; break;
				case 32: targ_text = "E♯♯"; break;
				case 33: targ_text = "B♯♯"; break;
			}
console.log("targ_text = " + targ_text);
var targ_color = targ_text;
if (targ_text == "E♯") targ_text = "F";
text.color = NOTE_COLOR[targ_text];
//console.log(text.color);
                        text.pos.y = 9.20;
			if (notes[i].pitch == 77 || notes[i].pitch == 78 || notes[i].pitch <= 69 && notes[i].pitch >= 67) {
//				text.pos.y = 1.1;
			} else if (notes[i].pitch == 79) {
                                text.pos.y = 8.68;
				text.pos.x = -1.3;
			} else if (notes[i].pitch > 78) {
				//text.pos.y = 1.65 - (notes[i].pitch-78)*0.39;
                                text.pos.y = 8.68;
                                text.pos.x = -0.7;
				if (notes[i].pitch <= 80) {
				//	text.pos.y -= 0.5;
				}
			}
			if (notes[i].tpc > 33 || notes[i].tpc < -1) {
				text.text = qsTr("?")	+ text.text; break;
				//console.log("error");
			} else {
				if (notes[i].pitch < 67) {
					text.text = '𑄲' + qsTranslate("InspectorAmbitus", targ_text);
text.pos.y = 8.68;
                                text.pos.x = -0.7;
				} else if (notes[i].pitch > 78) {
					text.text = qsTranslate("InspectorAmbitus", targ_text).toLowerCase() + text.text;
					text.text = "𑄩"+qsTranslate("InspectorAmbitus", targ_text);
				} else {
					text.text = qsTranslate("InspectorAmbitus", targ_text) + text.text;
				}
			}

			console.log(notes[i].pitch + " becomes " + text.text + "\nwith y: " + text.pos.y);

// change below false to true for courtesy- and microtonal accidentals
// you might need to come up with suitable translations
// only #, b, natural and possibly also ## seem to be available in UNICODE
			if (false) {
				switch (notes[i].userAccidental) {
					case  0: break;
					case  1: text.text = qsTranslate("accidental", "Sharp") + text.text; break;
					case  2: text.text = qsTranslate("accidental", "Flat") + text.text; break;
					case  3: text.text = qsTranslate("accidental", "Double sharp") + text.text; break;
					case  4: text.text = qsTranslate("accidental", "Double flat") + text.text; break;
					case  5: text.text = qsTranslate("accidental", "Natural") + text.text; break;
					case  6: text.text = qsTranslate("accidental", "Flat-slash") + text.text; break;
					case  7: text.text = qsTranslate("accidental", "Flat-slash2") + text.text; break;
					case  8: text.text = qsTranslate("accidental", "Mirrored-flat2") + text.text; break;
					case  9: text.text = qsTranslate("accidental", "Mirrored-flat") + text.text; break;
					case 10: text.text = qsTranslate("accidental", "Mirrored-flat-slash") + text.text; break;
					case 11: text.text = qsTranslate("accidental", "Flat-flat-slash") + text.text; break;
					case 12: text.text = qsTranslate("accidental", "Sharp-slash") + text.text; break;
					case 13: text.text = qsTranslate("accidental", "Sharp-slash2") + text.text; break;
					case 14: text.text = qsTranslate("accidental", "Sharp-slash3") + text.text; break;
					case 15: text.text = qsTranslate("accidental", "Sharp-slash4") + text.text; break;
					case 16: text.text = qsTranslate("accidental", "Sharp arrow up") + text.text; break;
					case 17: text.text = qsTranslate("accidental", "Sharp arrow down") + text.text; break;
					case 18: text.text = qsTranslate("accidental", "Sharp arrow both") + text.text; break;
					case 19: text.text = qsTranslate("accidental", "Flat arrow up") + text.text; break;
					case 20: text.text = qsTranslate("accidental", "Flat arrow down") + text.text; break;
					case 21: text.text = qsTranslate("accidental", "Flat arrow both") + text.text; break;
					case 22: text.text = qsTranslate("accidental", "Natural arrow down") + text.text; break;
					case 23: text.text = qsTranslate("accidental", "Natural arrow up") + text.text; break;
					case 24: text.text = qsTranslate("accidental", "Natural arrow both") + text.text; break;
					case 25: text.text = qsTranslate("accidental", "Sori") + text.text; break;
					case 26: text.text = qsTranslate("accidental", "Koron") + text.text; break;
					default: text.text = qsTr("?") + text.text; break;
				} // end switch userAccidental
			} // end if courtesy- and microtonal accidentals
		} // end for note
	}

	onRun: {
		if (typeof curScore === 'undefined')
			Qt.quit();

		var cursor = curScore.newCursor();
		var startStaff;
		var endStaff;
		var endTick;
		var fullScore = false;
		cursor.rewind(1);
		if (!cursor.segment) { // no selection
			fullScore = true;
			startStaff = 0; // start with 1st staff
			endStaff  = curScore.nstaves - 1; // and end with last
		} else {
			startStaff = cursor.staffIdx;
			cursor.rewind(2);
			if (cursor.tick === 0) {
				// this happens when the selection includes
				// the last measure of the score.
				// rewind(2) goes behind the last segment (where
				// there's none) and sets tick=0
				endTick = curScore.lastSegment.tick + 1;
			} else {
				endTick = cursor.tick;
			}
			endStaff = cursor.staffIdx;
		}
		console.log(startStaff + " - " + endStaff + " - " + endTick)

		for (var staff = startStaff; staff <= endStaff; staff++) {
			for (var voice = 0; voice < 4; voice++) {
				cursor.rewind(1); // beginning of selection
				cursor.voice	 = voice;
				cursor.staffIdx = staff;

				if (fullScore)  // no selection
					cursor.rewind(0); // beginning of score

				while (cursor.segment && (fullScore || cursor.tick < endTick)) {
					if (cursor.element && cursor.element.type === Element.CHORD) {
						var text = newElement(Element.STAFF_TEXT);

						var graceChords = [];//cursor.element.graceNotes;
						for (var i = 0; i < graceChords.length; i++) {
							// iterate through all grace chords
							var graceNotes = graceChords[i].notes;
							nameChord(graceNotes, text);
							// there seems to be no way of knowing the exact horizontal pos.
							// of a grace note, so we have to guess:
							text.pos.x = -2.5 * (graceChords.length - i);
							switch (voice) {
							//case 0: text.pos.y -=  -95; break;
								case 1: text.pos.y = 10; break;
								case 2: text.pos.y = -1; break;
								case 3: text.pos.y = 12; break;
							}

							cursor.add(text);
							// new text for next element
							text  = newElement(Element.STAFF_TEXT);
						}

						var notes = cursor.element.notes;
						nameChord(notes, text);

						switch (voice) {
							//case 0: text.pos.y =  1; break;
							case 1: text.pos.y = 10; break;
							case 2: text.pos.y = -1; break;
							case 3: text.pos.y = 12; break;
						}
//						if ((voice == 0) && (notes[0].pitch > 78))
//							text.pos.x = 0.3;
						cursor.add(text);
					} // end if CHORD
					cursor.next();
				} // end while segment
			} // end for voice
		} // end for staff
		Qt.quit();
	} // end onRun
}
