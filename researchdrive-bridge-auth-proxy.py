#!/usr/bin/env python3
import sys, json, os, re, requests, subprocess

data = json.load(sys.stdin)
user = data["user"]
password = data["pass"]

if not re.fullmatch(r"[A-Za-z0-9_.@-]+", user):
    sys.exit(1)

base_url = os.environ["NEXTCLOUD_BASE_URL"]
nextcloud_url = base_url + "/remote.php/dav/files/" + user + "/"

try:
    check = requests.request(
        "PROPFIND", nextcloud_url, auth=(user, password), timeout=10
    )
except requests.RequestException:
    sys.exit(1)

if check.status_code not in (207, 200):
    sys.exit(1)
 
#https://rclone.org/commands/rclone_obscure/ 
obscured = subprocess.run(
    ["rclone", "obscure", password],
    capture_output=True, text=True, check=True
).stdout.strip()


def rclone_quote(value):
    return "'" + value.replace("'", "''") + "'"


connection_string = ":webdav,url={},vendor=nextcloud,user={},pass={}:".format(
    rclone_quote(nextcloud_url), rclone_quote(user), rclone_quote(obscured)
)

config = {
    "type": "combine",
    "upstreams": "nextcloud-root-directory=" + connection_string,
    "_root": ""
}

print(json.dumps(config))
