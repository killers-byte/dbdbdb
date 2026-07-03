# 🔥 BIN AI Offensive Suite

**Terminal Kecerdasan Buatan + Pusat Komando Serangan Siber**  
Dibangun di atas Google Gemini, diperkuat dengan senjata ofensif open-source.  
Kendalikan seluruh operasi hanya dengan satu chat.

---

## 🧠 Deskripsi

BIN AI adalah asisten intelijen digital pribadi yang menggabungkan **AI percakapan canggih** (Gemini Flash) dengan **arsenal keamanan ofensif** (nmap, sqlmap, hydra, searchsploit, holehe, sherlock, dan banyak lagi). Semua diakses melalui antarmuka terminal cyberpunk yang responsif.

Proyek ini dirancang untuk **simulasi keamanan, pengujian penetrasi, riset intelijen, dan operasi ofensif yang sah**. Pemilik bertanggung jawab penuh atas penggunaan.

---

## ⚡ Fitur Unggulan

- **Chat AI Real-Time** – diskusi bebas dengan Gemini Flash, tanpa sensor.
- **Reconnaissance Otomatis** – `/recon` menjalankan nmap + analisis AI.
- **Pemindaian Kerentanan** – `/vulnscan` memanfaatkan NSE & searchsploit.
- **Bruteforce Service** – `/hydrabrute` dengan Hydra.
- **OSINT Mendalam** – `/osint` menggabungkan holehe & sherlock.
- **Cari Exploit** – `/searchsploit` langsung dari database lokal.
- **Social Engineering Generator** – `/socialeng` hasilkan skenario phishing AI.
- **Pelacakan Presisi** – `/track` nomor HP, email, username, lengkap dengan koordinat & Google Maps.
- **Tampilan Cyberpunk Matrix** – efek latar real-time, avatar bot & user.
- **Backend Tunggal** – Express.js menyajikan frontend & API, tanpa masalah CORS.

---

## 📋 Daftar Command

| ----------------|-----------------------------------------------------------------------|
| Command         | Fungsi                                                                |
|-----------------|-----------------------------------------------------------------------|
| `/help`         | Tampilkan semua command                                               |
| `/recon`        | Pemindaian nmap + analisis AI                                         |
| `/vulnscan`     | Pemindaian kerentanan + rekomendasi exploit                           |
| `/exploit`      | Eksekusi modul Metasploit (jika tersedia)                             |
| `/hydrabrute`   | Bruteforce login layanan                                              |
| `/osint`        | Penyelidikan email/username (holehe + sherlock)                       |
| `/searchsploit` | Pencarian exploit di database lokal                                   |
| `/socialeng`    | Buat skenario phishing sesuai target                                  |
| `/track`        | Lacak nomor HP, email, atau username + koordinat satelit & Google Maps|

---

## 🛠️ Prasyarat

- **Node.js** ≥ 18.x
- **Python** ≥ 3.10
- **Tools eksternal** (install otomatis via `install.sh`):
  - nmap, sqlmap, hydra, gobuster, whatweb, git
  - searchsploit (ExploitDB)
  - holehe, sherlock
  - Python libraries: `phonenumbers`, `geopy`, `requests`, `python-dotenv`

---

## 🚀 Instalasi Cepat

1. **Clone repository**  
   ```bash
   git clone https://github.com/username/BIN-AI-Offensive.git
   cd BIN-AI-Offensive
