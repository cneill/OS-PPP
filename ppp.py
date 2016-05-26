#!/usr/bin/env python
"""OpenStack PPP Generator :)

Usage:
    ./ppp.py generate <username> [<project>]

Options:
    generate       Generate a PPP email from the last week
    <username>     OpenStack username
    <project>      OpenStack project [default: openstack/syntribos]
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

    def __init__(self, username=None, user_id=None, project_name=None,
                 base_url=None, default_delta=None, after=None):
        self.base_url = base_url if base_url else self.base_url
        self.user_search = urllib.quote(user_id if user_id else username)
        self.project_name = project_name if project_name else self.project_name
        self.project_search = urllib.quote(
            project_name if project_name else self.project_name, safe="")
        self.default_delta = (
            default_delta if default_delta else self.default_delta)
        self.after = (
            after if after else (datetime.datetime.now().replace(tzinfo=HERE).astimezone(UTC) - self.default_delta))

        if not user_id and not username:
            sys.exit("NO VALID USER SPECIFIED")

        self.user_obj = self.get_user_obj()
        self.project_obj = self.get_project_obj()

        if not self.user_obj:
            sys.exit("COULD NOT FIND USER")

        if not self.project_obj:
            sys.exit("COULD NOT FIND PROJECT")

        self.gather_project_changes()

    @classmethod
    def request(cls, method, path):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        url = ""
        response = None
        j_contents = None

        url = "{0}{1}".format(cls.base_url, path)

        try:
            response = requests.request(method, url, headers=headers)
        except Exception as e:
            print "Oops.\n", e
            sys.exit()

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

    def get_change_reviewers(self, change):
        change_id = change["change_id"]
        return self.request("GET", "/changes/{0}/reviewers".format(change_id))

    def get_change_url(self, change):
        return "{0}/#/c/{1}".format(self.base_url, change["_number"])

    def did_code_review(self, change):
        reviewers = self.get_change_reviewers(change)
        for r in reviewers:
            if r["_account_id"] == self.user_obj["_account_id"]:
                if r.get("approvals"):
                    if r["approvals"].get("Code-Review"):
                        return True
                else:
                    return False

    def owns(self, change):
        return change["owner"]["_account_id"] == self.user_obj["_account_id"]

    def gather_project_changes(self):
        after_str = self.after.strftime("%Y-%m-%d")
        path = "/changes/?q=project:{0}%20after:{1}".format(
            self.project_search, after_str)
        self.project_changes = results = self.request("GET", path)
        for r in results:
            if r["status"] == "MERGED":
                self.merged_changes.append(r)
            elif r["status"] == "ABANDONED":
                self.abandoned_changes.append(r)
            elif r["status"] in ["NEW", "PENDING", "REVIEWED"]:
                self.open_changes.append(r)
            else:
                print r["status"]

    def print_change(self, change, time_pat="%Y-%m-%d %H:%M:%S"):
        print "- " + change["subject"]
        print "\tURL: {0}".format(self.get_change_url(change))
        print "\tLast updated: ",
        print_local_time(change["updated"])


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
        if OSA.owns(change):
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
            lines["code_review_insertion"] += change["insertions"]
            lines["code_review_deletion"] += change["deletions"]
    print "\nLines: +{0} -{1}\n".format(
        lines["code_review_insertion"], lines["code_review_deletion"])

    print SEP

    print "Recent open change requests from {0}:\n".format(OSA.user_obj["name"])
    for change in OSA.open_changes:
        if OSA.owns(change):
            OSA.print_change(change)
            counts["open_crs"] += 1
            lines["open_cr_insertion"] += change["insertions"]
            lines["open_cr_deletion"] += change["deletions"]
    print "\nLines: +{0} -{1}\n".format(
        lines["open_cr_insertion"], lines["open_cr_deletion"])

    print SEP

    print "Total merged CRs: {0}".format(counts["merged_crs"])
    print "Total code reviews: {0}".format(counts["code_reviews"])
    print "Total open CRs: {0}".format(counts["open_crs"])
    total_insertions = lines["merged_cr_insertion"] + lines["code_review_insertion"]
    total_deletions = lines["merged_cr_deletion"] + lines["code_review_deletion"]
    print "Total merged lines: +{0} -{1}".format(total_insertions, total_deletions)
    print "Total unmerged lines: +{0} -{1}".format(lines["open_cr_insertion"], lines["open_cr_deletion"])


def main(args):
    if args['generate'] and args['<username>']:
        if args['<project>']:
            OSA = OSAPI(
                username=args['<username>'], project_name=args['<project>'])
        else:
            OSA = OSAPI(username=args['<username>'])
        generate_PPP(OSA)

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
