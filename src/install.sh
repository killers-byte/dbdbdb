#!/bin/bash
# ==========================================
# BIN AI Offensive Suite - Instalasi Tool
# ==========================================

echo "🔥 Mulai instalasi senjata ofensif..."

sudo apt update -y

# Paket dasar
sudo apt install -y nmap sqlmap hydra whois gobuster whatweb git curl wget python3-pip

# Library Python untuk tracker & AI analyzer
pip3 install holehe phonenumbers geopy requests

# ExploitDB / searchsploit (jika belum ada)
if ! command -v searchsploit &> /dev/null; then
    echo "📦 Menginstall searchsploit dari GitLab..."
    sudo rm -rf /opt/exploitdb
    sudo git clone https://gitlab.com/exploit-database/exploitdb.git /opt/exploitdb
    sudo chmod +x /opt/exploitdb/searchsploit
    sudo ln -sf /opt/exploitdb/searchsploit /usr/local/bin/searchsploit
    searchsploit -u
else
    echo "✅ searchsploit sudah terpasang."
fi

# Sherlock (OSINT username)
if ! command -v sherlock &> /dev/null; then
    echo "🕵️ Menginstall Sherlock..."
    sudo rm -rf /opt/sherlock
    sudo git clone https://github.com/sherlock-project/sherlock.git /opt/sherlock
    cd /opt/sherlock
    sudo pip3 install .
    sudo ln -sf /opt/sherlock/sherlock.py /usr/local/bin/sherlock
    cd -
else
    echo "✅ Sherlock sudah terpasang."
fi

echo "✅ Semua tools siap digunakan."
echo "Sekarang jalankan: node server.js"
