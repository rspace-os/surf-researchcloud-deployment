#!/usr/bin/env python3
import sys, json, os, requests, subprocess
 
data = json.load(sys.stdin)
user = data["user"]
password = data["pass"]
 
base_url = os.environ["NEXTCLOUD_BASE_URL"]
nextcloud_url = base_url + "/remote.php/dav/files/" + user + "/"
 
check = requests.request("PROPFIND", nextcloud_url, auth=(user, password))
if check.status_code not in (207, 200):
    sys.exit(1)
 
obscured = subprocess.run(
    ["rclone", "obscure", password],
    capture_output=True, text=True, check=True
).stdout.strip()
 
connection_string = ":webdav,url='{}',vendor=nextcloud,user='{}',pass='{}':".format(
    nextcloud_url, user, obscured
)
 
config = {
    "type": "combine",
    "upstreams": "nextcloud-root-directory=" + connection_string,
    "_root": ""
}
 
print(json.dumps(config))
 
