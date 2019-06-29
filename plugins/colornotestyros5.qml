//=============================================================================
//  MuseScore
//  Music Composition & Notation
//
//  Copyright (C) 2012 Werner Schweer
//  Copyright (C) 2013-2015 Nicolas Froment, Joachim Schmitz
//  Copyright (C) 2014 Jörn Eichler
//  Copyright (C) 2015 Sylvain Kuntzmann
//
//  This program is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License version 2
//  as published by the Free Software Foundation and appearing in
//  the file LICENCE.GPL
//=============================================================================

import QtQuick 2.0
import MuseScore 1.0

MuseScore {
      version:  "1.0"
      description: "This plugin colors notes in the selection depending on pitch and according to the Yamaha Tyros 5."
      menuPath: "Plugins.Notes.Color Notes Tyros5"

      property variant colors : [
               "#C60800", "#df7500", "#F6DC12", // do, do#, ré
               "#bfaf3f", "#3A9D23", "#582900", // ré#, mi, fa
               "#6faf4b", "#22427C", "#a38cb9", // fa#, sol, sol#
               "#318CE7", "#75d0c8", "#000000"  // la, la#, si
               ]
      property variant black : "#000000"

      // Apply the given function to all notes in selection
      // or, if nothing is selected, in the entire score

      function applyToNotesInSelection(func) {
            var cursor = curScore.newCursor();
            cursor.rewind(1);
            var startStaff;
            var endStaff;
            var endTick;
            var fullScore = false;
            if (!cursor.segment) { // no selection
                  fullScore = true;
                  startStaff = 0; // start with 1st staff
                  endStaff = curScore.nstaves - 1; // and end with last
            } else {
                  startStaff = cursor.staffIdx;
                  cursor.rewind(2);
                  if (cursor.tick == 0) {
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
                        cursor.rewind(1); // sets voice to 0
                        cursor.voice = voice; //voice has to be set after goTo
                        cursor.staffIdx = staff;

                        if (fullScore)
                              cursor.rewind(0) // if no selection, beginning of score

                        while (cursor.segment && (fullScore || cursor.tick < endTick)) {
                              if (cursor.element && cursor.element.type == Element.CHORD) {
                                    var graceChords = cursor.element.graceNotes;
                                    for (var i = 0; i < graceChords.length; i++) {
                                          // iterate through all grace chords
                                          var notes = graceChords[i].notes;
                                          for (var j = 0; j < notes.length; j++)
                                                func(notes[j]);
                                    }
                                    var notes = cursor.element.notes;
                                    for (var i = 0; i < notes.length; i++) {
                                          var note = notes[i];
                                          func(note);
                                    }
                              }
                              cursor.next();
                        }
                  }
            }
      }

      function colorNote(note) {
            //if (note.color == black)
                  note.color = colors[note.pitch % 12];
/*            else
                  note.color = black;*/

            if (note.accidental) {
    //              if (note.accidental.color == black)
                        note.accidental.color = colors[note.pitch % 12];
      /*            else
                        note.accidental.color = black;*/
                  }

            for (var i = 0; i < note.dots.length; i++) {
                  if (note.dots[i]) {
                       // if (note.dots[i].color == black)
                              note.dots[i].color = colors[note.pitch % 12];
                        /*else
                              note.dots[i].color = black;*/
                        }
                  }
         }

      onRun: {
            console.log("hello colornotes for Yamaha Tyros5");

            if (typeof curScore === 'undefined')
                  Qt.quit();

            applyToNotesInSelection(colorNote)

            Qt.quit();
         }
}
