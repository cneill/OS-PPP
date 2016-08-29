# PPP!

__Install:__

```
mkvirtualenv <env>
pip install -r requirements.txt
```

__Usage:__

```
OpenStack PPP Generator :)

Usage:
    ./ppp.py [-v] generate <username> [<project>]

Options:
    generate       Generate a PPP email from the last week
    <username>     OpenStack username
    <project>      OpenStack project [default: openstack/syntribos]
    --verbose, -v  Verbose output
    --help         Display this help message
```

__Example Output:__

```
$ ./ppp.py generate cneill openstack/syntribos

Activity on openstack/syntribos since  2016-08-22 18:23:52

Merged change requests owned by Charles Neill:

- Minor fixup to readme
        URL: https://review.openstack.org/#/c/360132
        Last updated:  2016-08-25 15:33:28
- Refresh readme
        URL: https://review.openstack.org/#/c/360123
        Last updated:  2016-08-24 19:15:40
- Fixes a bug in "excluded tests"
        URL: https://review.openstack.org/#/c/353784
        Last updated:  2016-08-24 18:25:58

Lines: +88 -48

================================================================================
Merged changes code reviewed by Charles Neill:

- Modifying log file path
        URL: https://review.openstack.org/#/c/362427
        Last updated:  2016-08-29 18:22:09
- Minor nit in progress display
        URL: https://review.openstack.org/#/c/362484
        Last updated:  2016-08-29 18:17:34

...

Lines: +894 -5984

================================================================================
Unmerged changes from Charles Neill:

- Adds relative paths for templates
        URL: https://review.openstack.org/#/c/362460
        Last updated:  2016-08-29 18:22:42
        Owner: Charles Neill
        Jenkins: +1 (Works for me)
        Code Review Status:  0 (No score)
        Merge status: MERGEABLE
- Removing "config-dir", modifying "config-file"
        URL: https://review.openstack.org/#/c/348589
        Last updated:  2016-08-29 18:22:17
        Owner: Charles Neill
        Jenkins: -1 (Doesn't seem to work)
        Code Review Status:  0 (No score)
        Merge status: MERGE CONFLICT

Lines: +178 -30

================================================================================
Unmerged changes code reviewed by Charles Neill:

- Fixed runner time log
        URL: https://review.openstack.org/#/c/362480
        Last updated:  2016-08-29 17:49:21
        Owner: Michael Dong
        Jenkins: +1 (Works for me)
        Code Review Status: -1 (This patch needs further work before it can be merged)
        Merge status: MERGEABLE
================================================================================
Total merged CRs: 3
Total code reviews: 13
Total code review comments: 42
Total open CRs: 2
Total merged lines: +982 -6032
Total unmerged lines: +178 -30
```
