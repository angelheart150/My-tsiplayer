
#!/bin/sh
##############################################################
# TSIPlayer Auto Installer from GitHub Repo by Mohamed Elsafty
# Version: 1.0
# Description: Download latest host_*.py files and back up old ones
#setup command=wget -q "--no-check-certificate" https://github.com/angelheart150/My-tsiplayer/raw/main/install-tsiplayer-update-hosts.sh -O - | /bin/sh
##############################################################

echo ''
echo '************************************************************'
echo '**         TSIPlayer Hosts Update Script                  **'
echo '************************************************************'
echo '**         Uploaded by: Mohamed Elsafty                   **'
echo '************************************************************'
sleep 2s

DEST_DIR="/usr/lib/enigma2/python/Plugins/Extensions/IPTVPlayer/tsiplayer"
TMP_DIR="/var/volatile/tmp/mytsiplayer"
REPO_URL="https://github.com/angelheart150/My-tsiplayer"
DATE=$(date +%Y%m%d)

COUNT=0
UPDATED_FILES=""

echo "> Removing any previous temporary folder..."
rm -rf "$TMP_DIR"
mkdir -p "$TMP_DIR"

echo "> Downloading latest version from GitHub..."
wget -q --no-check-certificate https://github.com/angelheart150/My-tsiplayer/archive/refs/heads/main.zip -O "$TMP_DIR/main.zip"

if [ ! -f "$TMP_DIR/main.zip" ]; then
    echo "!! Failed to download the zip file. Check internet connection or URL."
    exit 1
fi

echo "> Extracting..."
unzip -q "$TMP_DIR/main.zip" -d "$TMP_DIR"

# Backup and replace host_*.py files
for file in "$TMP_DIR"/My-tsiplayer-main/host_*.py; do
    filename=$(basename "$file")
    destfile="$DEST_DIR/$filename"
    if [ -f "$destfile" ]; then
        echo "Backing up $filename to $filename.$DATE.bak"
        mv "$destfile" "$destfile.$DATE.bak"
    fi
    echo "Installing $filename"
    cp -f "$file" "$DEST_DIR/"
    COUNT=$((COUNT+1))
    UPDATED_FILES="$UPDATED_FILES\n$filename"
done

# Clean up temporary files
rm -rf "$TMP_DIR"
echo "> Temporary files cleaned up."

sync
echo '************************************************************'
echo "**      INSTALLATION DONE - $COUNT file(s) updated          **"
echo '************************************************************'
echo -e "Updated files:$UPDATED_FILES"
sleep 2

echo "Restarting Enigma2..."
killall -9 enigma2

exit 0
