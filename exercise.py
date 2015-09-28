#! /src/bin/env python
# encoding: utf-8

# Utilities for Moodle Scraping
import re

class MoodleExercise:
    """ encapsulates a moodle exercise """

    def __init__(self, name, description):
        self.id_moodle = None
        self.data = {
            "id_name": name,
            "id_introeditor": description,
            "id_showdescription": False,                # Mostra la descripció a la pàgina principal del curs
            "id_allowsubmissionsfromdate_enabled": False,
            "id_duedate_enabled": False,
            "id_cutoffdate_enabled": False,
            "id_alwaysshowdescription": False,
            "id_assignsubmission_onlinetext_enabled": None,
            "id_assignsubmission_file_enabled": None,
            "id_assignsubmission_onlinetext_wordlimit": None,
            "id_assignsubmission_onlinetext_wordlimit_enabled": None,
            "id_assignfeedback_comments_enabled": None,
            "id_assignfeedback_file_enabled": None,
            "id_assignfeedback_offline_enabled": None,
            "id_modgrade_point": None,
            "id_cmidnumber": None,
            "id_cancel": None,
            "id_allowsubmissionsfromdate_day": None,
            "id_allowsubmissionsfromdate_month": None,
            "id_allowsubmissionsfromdate_year": None,
            "id_allowsubmissionsfromdate_hour": None,
            "id_allowsubmissionsfromdate_minute": None,
            "id_duedate_day": None,
            "id_duedate_month": None,
            "id_duedate_year": None,
            "id_duedate_hour": None,
            "id_duedate_minute": None,
            "id_cutoffdate_day": None,
            "id_cutoffdate_month": None,
            "id_cutoffdate_year": None,
            "id_cutoffdate_hour": None,
            "id_cutoffdate_minute": None,
            "id_assignsubmission_file_maxfiles": None,
            "id_assignsubmission_file_maxsizebytes": None,
            "id_assignfeedback_comments_commentinline": None,
            "id_submissiondrafts": None,
            "id_requiresubmissionstatement": None,
            "id_attemptreopenmethod": None,
            "id_maxattempts": None,
            "id_teamsubmission": None,
            "id_requireallteammemberssubmit": None,
            "id_teamsubmissiongroupingid": None,
            "id_sendnotifications": None,
            "id_sendlatenotifications": None,
            "id_sendstudentnotifications": None,
            "id_modgrade_type": None,
            "id_modgrade_scale": None,
            "id_advancedgradingmethod_submissions": None,
            "id_gradecat": None,
            "id_blindmarking": None,
            "id_markingworkflow": None,
            "id_markingallocation": None,
            "id_visible": [ "0" ],
            "id_groupmode": None,
            "id_groupingid": None,
        }

    def set_allowsubmissionsfromdate(self, date):
        """ sets allowsubmissionsfrom date """
        self._set_date("allowsubmissionsfromdate", date)

    def set_duedate(self, date):
        """ sets due date """
        self._set_date("duedate", date)

    def set_cutoffdate(self, date):
        """ sets cutoff date """
        self._set_date("cutoffdate", date)

    def _set_date(self, key, date):
        """ date is a string in the form dd/mm/yyyy hh:mm"""
        postkey_options = [ "day", "month", "year", "hour", "minute" ]
        m = re.match("(\d+)\D(\d+)\D(\d+)\D(\d+)\D(\d+)", date)
        if not m:
            print "Error: not a date '%s'"%date
            sys.exit()
        for i in range(len(postkey_options)):
            if "id_%s_%s"%(key, postkey_options[i]) not in self.data:
                print "XXX errror"

            self.data["id_%s_%s"%(key, postkey_options[i])]=[m.group(i+1)]
        self.data["id_%s_enabled"%key]=True


