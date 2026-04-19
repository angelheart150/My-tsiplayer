#!/bin/sh
##############################################################
# TSIPlayer Auto Installer + Hosts Updater from GitHub Repo
# By Mohamed Elsafty
# Version: 2.0
# Description: Update host_*.py files and keep latest .bak only
#setup command=wget -q "--no-check-certificate" https://github.com/angelheart150/My-tsiplayer/raw/main/install-tsiplayer-update-hosts.sh -O - | /bin/sh
##############################################################
echo ''
echo '************************************************************'
echo '**         TSIPlayer Installer / Updater                  **'
echo '************************************************************'
echo '**         Uploaded by: Mohamed Elsafty                   **'
echo '************************************************************'
sleep 2
BASE_DIR="/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer"
DEST_DIR="$BASE_DIR/tsiplayer"
TMP_DIR="/var/volatile/tmp/mytsiplayer"
REPO_URL="https://github.com/angelheart150/My-tsiplayer"
ARCHIVE_URL="https://github.com/angelheart150/My-tsiplayer/raw/main/Tsiplayer.tar.gz"
DATE=$(date +%Y%m%d)
COUNT=0
UPDATED_FILES=""
echo "> Cleaning temp ..."
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"
##############################################################
# 1. INSTALL IF NOT EXISTS
##############################################################
if [ ! -d "$DEST_DIR" ]; then
    echo "> tsiplayer NOT found → Installing full package..."
    wget -q --no-check-certificate "$ARCHIVE_URL" -O "$TMP_DIR/Tsiplayer.tar.gz"
    if [ ! -f "$TMP_DIR/Tsiplayer.tar.gz" ]; then
        echo "!! Download failed"
        exit 1
    fi
    tar -xzf "$TMP_DIR/Tsiplayer.tar.gz" -C /
    echo "> Full installation done."
else
    echo "> tsiplayer exists → skipping install"
fi
##############################################################
# 🔹 SMART ARABIC GROUP SYNC + TSIPLAYER AUTO ADD
##############################################################
GROUP_FILE="/etc/enigma2/iptvplayerarabicgroup.json"
HOSTGROUPS_FILE="/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/hosts/hostgroups.txt"
HOST="tsiplayer"
echo "> Processing Arabic favorites smart sync..."
python - <<EOF
import json
import re
import os
group_file = "$GROUP_FILE"
hostgroups_file = "$HOSTGROUPS_FILE"
host = "$HOST"
# -----------------------------
# CASE 1: FILE EXISTS
# -----------------------------
if os.path.exists(group_file):
    try:
        with open(group_file, "r") as f:
            data = json.load(f)
    except:
        data = {"version": 0, "hosts": [], "disabled_hosts": []}
    if "hosts" not in data:
        data["hosts"] = []
    if host not in data["hosts"]:
        data["hosts"].append(host)
# -----------------------------
# CASE 2: FILE NOT EXISTS
# -----------------------------
else:
    arabic_hosts = []
    try:
        with open(hostgroups_file, "r") as f:
            txt = f.read()
        match = re.search(r'"arabic"\s*:\s*\[(.*?)\]', txt, re.S)
        if match:
            arabic_hosts = re.findall(r'"(.*?)"', match.group(1))
    except:
        arabic_hosts = []
    if host not in arabic_hosts:
        arabic_hosts.append(host)
    data = {
        "version": 0,
        "hosts": arabic_hosts,
        "disabled_hosts": []
    }
# -----------------------------
# SAVE RESULT
# -----------------------------
with open(group_file, "w") as f:
    json.dump(data, f)
print("> Arabic group synced + tsiplayer added successfully")
EOF
##############################################################
# 🔹 2. ALWAYS UPDATE HOSTS (IMPORTANT FIX)
##############################################################
echo "> Updating hosts..."
wget -q --no-check-certificate "$REPO_URL/archive/refs/heads/main.zip" -O "$TMP_DIR/main.zip"
if [ ! -f "$TMP_DIR/main.zip" ]; then
    echo "!! Download failed"
    exit 1
fi
unzip -q "$TMP_DIR/main.zip" -d "$TMP_DIR"
EXTRACTED="$TMP_DIR/My-tsiplayer-main"
for file in "$EXTRACTED"/host_*.py; do
    filename=$(basename "$file")
    destfile="$DEST_DIR/$filename"
    echo "> Processing $filename"
	# Remove old backups except today
    find "$DEST_DIR" -maxdepth 1 -type f -name "$filename.*.bak" ! -name "$filename.$DATE.bak" -exec rm -f {} \;
	# Backup current version if exists
    if [ -f "$destfile" ]; then
        echo "  - Backup old version"
        mv "$destfile" "$destfile.$DATE.bak"
    fi
    # copy new host
    cp -f "$file" "$destfile"
    COUNT=$((COUNT+1))
    UPDATED_FILES="$UPDATED_FILES\n$filename"
done
##############################################################
# Clean up temporary files
##############################################################
echo "> Cleaning temp..."
rm -rf "$TMP_DIR"
sleep 1
echo "> Temporary files cleaned up."
sync
echo '************************************************************'
echo "**      DONE - $COUNT file(s) updated                      **"
echo '************************************************************'
echo -e "Updated files:$UPDATED_FILES"
sleep 2
##############################################################
# 🔹 Restart Enigma2
##############################################################
echo "> Restarting Enigma2..."
sync
sleep 2
killall -9 enigma2
exit 0