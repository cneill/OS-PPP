# PPP!

__Install:__

```
mkvirtualenv <env>
pip install -r requirements.txt
```

__Usage:__

`./ppp.py generate <OpenStack username>`

__Example Output:__

```
$ ./ppp.py generate cneill

Activity since  2016-05-18 11:26:54

Merged change requests owned by Charles Neill

- Adding CAFE HTTP client install as tox docs step
	URL: https://review.openstack.org/#/c/317768
	Last updated:  2016-05-18 11:29:13

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
- Moved extend_class() function
	URL: https://review.openstack.org/#/c/318359
	Last updated:  2016-05-18 18:00:09
- Fixed payload truncating
	URL: https://review.openstack.org/#/c/318243
	Last updated:  2016-05-18 13:55:20
- Added String Validation Checks
	URL: https://review.openstack.org/#/c/318186
	Last updated:  2016-05-18 12:55:11

Recent open change requests from Charles Neill:

- Add exception/signal handling to HTTP client
	URL: https://review.openstack.org/#/c/317633
	Last updated:  2016-05-19 18:49:21
```
