#!/bin/bash
# SPEED PROOFS - Launcher Script
# This wraps DEMON-X to test the key first

BINARY="DEMON-X-final"
GIST_URL="https://gist.githubusercontent.com/karloays01-prog/dc667903c5fc4db6621f03c494a03816/raw/Fuckk"

echo "======================================"
echo "   SPEED PROOFS - Key Check System"
echo "======================================"
echo ""
echo "[*] Checking license from gist..."
echo "[*] URL: $GIST_URL"
echo ""

# Try to fetch the gist content
RESPONSE=$(curl -sSL --max-time 10 "$GIST_URL" 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "[!] Failed to connect to server"
    echo "[!] Check your internet connection"
    exit 1
fi

echo "[+] Got response from server"
echo "[+] Response: $RESPONSE"
echo ""

# Check if it contains valid data
if echo "$RESPONSE" | grep -q "V2"; then
    echo "✓ ACCESS GRANTED - License is valid!"
    echo ""
    echo "[*] Launching DEMON-X..."
    sleep 1
    ./"$BINARY"
else
    echo "✗ HACK IS EXPIRED"
    echo "[!] Your license has expired or is invalid"
    echo "[!] Please check your account on GitHub gists"
    exit 1
fi
