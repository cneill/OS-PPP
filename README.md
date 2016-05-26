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
    ./ppp.py generate <username> [<project>]

Options:
    generate       Generate a PPP email from the last week
    <username>     OpenStack username
    <project>      OpenStack project [default: openstack/syntribos]
    --help         Display this help message
```

__Example Output:__

```

$ ./ppp.py generate cneill

Activity since  2016-05-19 11:53:38

Merged change requests owned by Charles Neill:


Lines: +0 -0

================================================================================
Merged changes code reviewed by Charles Neill:

- Fix typo in authenticate_v3 parameter
	URL: https://review.openstack.org/#/c/321205
	Last updated:  2016-05-25 17:38:38
- Added SSL test case
	URL: https://review.openstack.org/#/c/318922
	Last updated:  2016-05-24 19:44:28
- Validate_length now checks status code
	URL: https://review.openstack.org/#/c/320561
	Last updated:  2016-05-24 17:36:10
- Started adding docstrings to extensions
	URL: https://review.openstack.org/#/c/317123
	Last updated:  2016-05-24 12:58:26
- Removed all_attacks
	URL: https://review.openstack.org/#/c/318767
	Last updated:  2016-05-19 17:07:40
- Modified buffer overflow attack
	URL: https://review.openstack.org/#/c/318207
	Last updated:  2016-05-19 16:13:11
- Modified integer overflow tests
	URL: https://review.openstack.org/#/c/318245
	Last updated:  2016-05-19 16:13:03
- Added CORS Header testcase
	URL: https://review.openstack.org/#/c/317147
	Last updated:  2016-05-19 16:11:34

Lines: +256 -1226

================================================================================
Recent open change requests from Charles Neill:

- Add exception/signal handling to HTTP client
	URL: https://review.openstack.org/#/c/317633
	Last updated:  2016-05-19 18:49:21

Lines: +300 -13

================================================================================
Total merged CRs: 0
Total code reviews: 8
Total open CRs: 1
Total merged line counts: +256 -1226
```
