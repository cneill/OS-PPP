#!/usr/bin/env python
"""OpenStack PPP Generator :)

Usage:
    ./ppp.py [-v] generate <username> [<project>]

Options:
    generate       Generate a PPP email from the last week
    <username>     OpenStack username
    <project>      OpenStack project [default: openstack/syntribos]
    --verbose, -v  Verbose output
    --help         Display this help message
"""


# import re
import datetime
import json
import pprint
import sys
import urllib

from dateutil import tz
from docopt import docopt
import requests

p = pprint.PrettyPrinter(indent=2)
HERE = tz.tzlocal()
UTC = tz.gettz("UTC")
SEP = "=" * 80


class OSAPI(object):

    project_name = "openstack/syntribos"
    base_url = "https://review.openstack.org"
    default_delta = datetime.timedelta(weeks=1)

    project_changes = []
    merged_changes = []
    abandoned_changes = []
    open_changes = []

    def _debug(self, string):
        if self.verbose:
            print "[DEBUG]\t" + string

    def __init__(self, username=None, user_id=None, project_name=None,
                 base_url=None, default_delta=None, after=None, verbose=False):
        self.base_url = base_url if base_url else self.base_url
        self.user_search = urllib.quote(user_id if user_id else username)
        self.project_name = project_name if project_name else self.project_name
        self.project_search = urllib.quote(
            project_name if project_name else self.project_name, safe="")
        self.default_delta = (
            default_delta if default_delta else self.default_delta)
        self.after = (
            after if after else (datetime.datetime.now().replace(tzinfo=HERE).astimezone(UTC) - self.default_delta))
        self.verbose = verbose

        if not user_id and not username:
            sys.exit("NO VALID USER SPECIFIED")

        self.user_obj = self.get_user_obj()
        self.project_obj = self.get_project_obj()

        if not self.user_obj:
            sys.exit("COULD NOT FIND USER")

        if not self.project_obj:
            sys.exit("COULD NOT FIND PROJECT")

        self.account_id = self.user_obj["_account_id"]

        self.gather_project_changes()

    def request(self, method, path):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        url = ""
        response = None
        j_contents = None

        url = "{0}{1}".format(self.base_url, path)

        try:
            self._debug("Requesting {url}...".format(url=url))
            response = requests.request(method, url, headers=headers)
        except Exception as e:
            print "Oops.\n", e
            sys.exit()
        self._debug("Got {url}...".format(url=url))

        contents = response.content[5:]

        try:
            j_contents = json.loads(contents)
        except ValueError as e:
            pass
        return j_contents

    def get_user_obj(self):
        resp = self.request("GET", "/accounts/{0}".format(self.user_search))
        if type(resp) is list and len(resp) > 1:
            return resp[0]
        return resp

    def get_project_obj(self):
        return self.request("GET", "/projects/{0}".format(self.project_search))

    def get_change_detail(self, change):
        change_id = change["change_id"]
        return self.request("GET", "/changes/{0}/detail".format(change_id))

    def get_change_reviewer_ids(self, change):
        result = []
        for review in change["labels"]["Code-Review"]["all"]:
            result.append(review["_account_id"])
        return result

    def has_owned_review_comments(self, change):
        return self.account_id in self.get_change_reviewer_ids(change)

    def get_review_comments(self, change):
        results = []
        if not self.has_owned_review_comments(change):
            return results

        for msg in change["messages"]:
            author = msg.get("author")
            if author and author["_account_id"] == self.account_id:
                results.append(msg)
        return results

    def get_change_url(self, change):
        return "{0}/#/c/{1}".format(self.base_url, change["_number"])

    def did_code_review(self, change):
        if self.owns_change(change):
            return False

        reviewers = self.get_change_reviewer_ids(change)
        for r in reviewers:
            if r == self.account_id:
                return True
        return False

    def owns_change(self, change):
        return change["owner"]["_account_id"] == self.account_id

    def gather_project_changes(self):
        after_str = self.after.strftime("%Y-%m-%d")
        path = "/changes/?q=project:{0}%20after:{1}".format(
            self.project_search, after_str)
        self.project_changes = self.request("GET", path)
        for change in self.project_changes:
            details = self.get_change_detail(change)
            if details["status"] == "MERGED":
                self.merged_changes.append(details)
            elif details["status"] == "ABANDONED":
                self.abandoned_changes.append(details)
            elif details["status"] in ["NEW", "PENDING", "REVIEWED"]:
                self.open_changes.append(details)
            else:
                print details["status"]

    def is_after(self, timestr):
        t = self.get_local_time(timestr)
        return t > self.after

    def get_review_value(self, val):
        if val == 0:
            return " 0"
        elif val == 1:
            return "+1"
        elif val == -1:
            return "-1"
        elif val == 2:
            return "+2"
        elif val == -2:
            return "-2"
        return " 0"

    def print_change(self, change, detailed=False, time_pat="%Y-%m-%d %H:%M:%S"):
        print "- {0}".format(change["subject"])
        print "\tURL: {0}".format(self.get_change_url(change))
        print "\tLast updated: ",
        print_local_time(change["updated"])

        if detailed:
            print "\tOwner: {0}".format(change["owner"]["name"])

            verified_val = self.get_review_value(change["labels"]["Verified"].get("value"))
            verified_text = change["labels"]["Verified"]["values"].get(str(verified_val), "None")
            print "\tJenkins: {val} ({text})".format(text=verified_text, val=verified_val)

            reviews = change["labels"]["Code-Review"]
            review_val = self.get_review_value(reviews.get("value"))
            review_text = reviews["values"].get(str(review_val), "None")
            print "\tCode Review Status: {val} ({text})".format(text=review_text, val=review_val)

            mergeable = change.get("mergeable", None)
            if mergeable is not None and not mergeable:
                print "\tMerge status: MERGE CONFLICT"
            else:
                print "\tMerge status: MERGEABLE"


def get_local_time(time_str, pat="%Y-%m-%d %H:%M:%S"):
    if "." in time_str:
        time_str = time_str.split(".")[0]
    d = datetime.datetime.strptime(time_str, pat)
    d = d.replace(tzinfo=UTC)
    d = d.astimezone(HERE)
    return d


def print_local_time(time_str, pat="%Y-%m-%d %H:%M:%S"):
    d = get_local_time(time_str, pat)
    print d.strftime(pat)


def generate_PPP(OSA):
    counts = {
        "merged_crs": 0,
        "code_reviews": 0,
        "code_review_comments": 0,
        "open_crs": 0
    }
    lines = {
        "merged_cr_insertion": 0,
        "merged_cr_deletion": 0,
        "code_review_insertion": 0,
        "code_review_deletion": 0,
        "open_cr_insertion": 0,
        "open_cr_deletion": 0
    }

    print "Activity on {0} since ".format(OSA.project_name),
    print_local_time(OSA.after.strftime("%Y-%m-%d %H:%M:%S"))
    print
    print "Merged change requests owned by {0}:\n".format(OSA.user_obj["name"])
    for change in OSA.merged_changes:
        if OSA.owns_change(change):
            OSA.print_change(change)
            counts["merged_crs"] += 1
            lines["merged_cr_insertion"] += change["insertions"]
            lines["merged_cr_deletion"] += change["deletions"]
    print "\nLines: +{0} -{1}\n".format(
        lines["merged_cr_insertion"], lines["merged_cr_deletion"])

    print SEP

    print "Merged changes code reviewed by {0}:\n".format(OSA.user_obj["name"])
    for change in OSA.merged_changes:
        if OSA.did_code_review(change):
            OSA.print_change(change)
            counts["code_reviews"] += 1
            counts["code_review_comments"] += len(OSA.get_review_comments(change))
            lines["code_review_insertion"] += change["insertions"]
            lines["code_review_deletion"] += change["deletions"]
    print "\nLines: +{0} -{1}\n".format(
        lines["code_review_insertion"], lines["code_review_deletion"])

    print SEP

    print "Unmerged changes from {0}:\n".format(OSA.user_obj["name"])
    for change in OSA.open_changes:
        if OSA.owns_change(change):
            OSA.print_change(change, detailed=True)
            counts["open_crs"] += 1
            lines["open_cr_insertion"] += change["insertions"]
            lines["open_cr_deletion"] += change["deletions"]
    print "\nLines: +{0} -{1}\n".format(
        lines["open_cr_insertion"], lines["open_cr_deletion"])

    print SEP

    print "Unmerged changes code reviewed by {0}:\n".format(OSA.user_obj["name"])
    for change in OSA.open_changes:
        if OSA.did_code_review(change) and OSA.has_owned_review_comments(change):
            OSA.print_change(change, detailed=True)
            counts["code_review_comments"] += len(OSA.get_review_comments(change))

    print SEP

    print "Total merged CRs: {0}".format(counts["merged_crs"])
    print "Total code reviews: {0}".format(counts["code_reviews"])
    print "Total code review comments: {0}".format(counts["code_review_comments"])
    print "Total open CRs: {0}".format(counts["open_crs"])
    total_insertions = lines["merged_cr_insertion"] + lines["code_review_insertion"]
    total_deletions = lines["merged_cr_deletion"] + lines["code_review_deletion"]
    print "Total merged lines: +{0} -{1}".format(total_insertions, total_deletions)
    print "Total unmerged lines: +{0} -{1}".format(lines["open_cr_insertion"], lines["open_cr_deletion"])


def main(args):
    if args["generate"] and args["<username>"]:
        project = args["<project>"] or ""
        OSA = OSAPI(username=args["<username>"], project_name=project, verbose=args["--verbose"])
        generate_PPP(OSA)

if __name__ == "__main__":
    args = docopt(__doc__)
    main(args)
