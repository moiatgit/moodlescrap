#! /src/bin/env python
# encoding: utf-8

# Test MoodleExercise class
from exercise import MoodleExercise

exercise = MoodleExercise("un", "dos")
exercise.set_allowsubmissionsfromdate("20/10/2016 14:55")
exercise.set_duedate("21/11/2017 15:50")
exercise.set_cutoffdate("19/9/2015 13:45")
print exercise.data

