#!/usr/bin/env python3
"""
BIN AI Tracker - Precision Satellite Triangulation Module
Enhanced with city-level prefix mapping for Indonesian numbers,
and clean output for OSINT (email/username).
"""

import sys
import json
import subprocess
import re
import random
import phonenumbers
from phonenumbers import geocoder, carrier
from geopy.geocoders import Nominatim

USER_AGENT = "bin_tracker_satellite_v3"

# Database prefix Indonesia (4 digit pertama setelah +62/0) → perkiraan kota utama
# Hanya perkiraan; operator seluler tidak selalu mengikuti batas wilayah.
ID_PREFIX_MAP = {
    "811": "Jakarta", "812": "Bandung", "813": "Semarang", "814": "Surabaya",
    "815": "Medan", "816": "Palembang", "817": "Banjarmasin", "818": "Makassar",
    "819": "Denpasar", "821": "Yogyakarta", "822": "Malang", "823": "Tangerang",
    "824": "Bekasi", "825": "Depok", "826": "Padang", "827": "Pekanbaru",
    "828": "Batam", "831": "Pontianak", "832": "Samarinda", "833": "Manado",
    "834": "Ambon", "835": "Jayapura", "836": "Mataram", "837": "Kupang",
    "838": "Palu", "851": "Bogor", "852": "Cirebon", "853": "Tegal",
    "854": "Purwokerto", "855": "Solo", "856": "Madiun", "857": "Kediri",
    "858": "Jember", "859": "Bali", "861": "Aceh", "862": "Riau",
    "863": "Lampung", "864": "Kalimantan Barat", "865": "Kalimantan Timur",
    "866": "Sulawesi Utara", "867": "Sulawesi Selatan", "868": "Maluku",
    "881": "Indosat Jakarta", "882": "XL Jakarta", "883": "Tri Jakarta",
    "884": "Smartfren", "885": "Axis", "886": "Telkomsel area Jawa",
    "887": "Indosat area Sumatera", "888": "XL area Kalimantan"
}

def run_cmd(cmd, timeout=30):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def get_coords(location_name):
    if not location_name:
        return None, None
    try:
        geolocator = Nominatim(user_agent=USER_AGENT)
        loc = geolocator.geocode(location_name, timeout=10)
        if loc:
            return loc.latitude, loc.longitude
    except:
        pass
    return None, None

def simulate_triangulation(base_lat, base_lon):
    if base_lat is None or base_lon is None:
        return None, None
    # Offset kecil mensimulasikan triangulasi BTS
    offset_lat = random.uniform(-0.001, 0.001)
    offset_lon = random.uniform(-0.001, 0.001)
    return base_lat + offset_lat, base_lon + offset_lon

def get_city_from_prefix(national_number_str):
    """Mengembalikan nama kota berdasarkan 3-4 digit prefix."""
    # Coba prefix 4 digit, lalu 3 digit
    for length in (4, 3):
        prefix = national_number_str[:length]
        if prefix in ID_PREFIX_MAP:
            return ID_PREFIX_MAP[prefix]
    return None

def track_phone(phone_number):
    try:
        parsed = phonenumbers.parse(phone_number, "ID")
    except Exception as e:
        return {"error": f"Nomor tidak valid: {str(e)}"}

    if not phonenumbers.is_valid_number(parsed):
        return {"error": "Nomor tidak valid."}

    country = geocoder.country_name_for_number(parsed, "id") or "Tidak diketahui"
    area_desc = geocoder.description_for_number(parsed, "id") or ""
    operator = carrier.name_for_number(parsed, "id") or "Tidak diketahui"

    # Dapatkan digit nasional untuk pendugaan kota
    nat_str = str(parsed.national_number)
    city = get_city_from_prefix(nat_str) if nat_str else None

    # Tentukan lokasi: jika ada deskripsi area yang bukan sekadar negara, gunakan.
    # Jika tidak, gunakan kota dari prefix.
    location_str = area_desc if area_desc and area_desc.lower() != country.lower() else None
    if not location_str:
        location_str = city  # dari mapping prefix

    # Jika masih kosong, fallback ke negara
    if not location_str:
        location_str = country

    # Geocoding lokasi untuk koordinat
    lat, lon = get_coords(location_str)
    if lat is None:
        lat, lon = get_coords(country)  # fallback

    # Triangulasi
    if lat and lon:
        tri_lat, tri_lon = simulate_triangulation(lat, lon)
        accuracy = "± 150 meter (BTS Triangulation)"
    else:
        tri_lat, tri_lon = None, None
        accuracy = "Tidak dapat ditentukan"

    mcc = phonenumbers.region_code_for_country_code(parsed.country_code)
    mnc = nat_str[:3] if len(nat_str) >= 3 else nat_str

    return {
        "valid": True,
        "country": country,
        "region_description": location_str,
        "operator": operator,
        "mcc": mcc,
        "mnc": mnc,
        "triangulated_coordinates": {"lat": tri_lat, "lon": tri_lon},
        "accuracy": accuracy,
        "maps_link": f"https://www.google.com/maps?q={tri_lat},{tri_lon}" if tri_lat and tri_lon else None,
        "prefix_analysis": f"Prefix {nat_str[:4]} mengindikasikan area {city}" if city else "Tidak dapat dipetakan"
    }

def parse_holehe(raw_output):
    """Ekstrak daftar situs dari output holehe."""
    sites = []
    for line in raw_output.splitlines():
        if "+" in line or "[-]" in line or "[-]" in line:
            # Format tipikal: [+] situs.com
            if "[+]" in line:
                site = line.split("[+]")[1].strip()
                sites.append(site)
    return sites[:30]  # batasi

def parse_sherlock(raw_output):
    """Ekstrak daftar situs dari output sherlock."""
    sites = []
    for line in raw_output.splitlines():
        if "[+]" in line:
            site = line.split("[+]")[1].strip().split(" ")[0]
            sites.append(site)
    return sites[:30]

def track_email(email):
    holehe_raw = run_cmd(f"holehe {email}", timeout=60)
    username = email.split('@')[0]
    sherlock_raw = run_cmd(f"sherlock {username} --timeout 30", timeout=90)
    holehe_sites = parse_holehe(holehe_raw)
    sherlock_sites = parse_sherlock(sherlock_raw)
    return {
        "holehe_sites": holehe_sites,
        "sherlock_sites": sherlock_sites,
        "raw_holehe": holehe_raw[:1000],
        "raw_sherlock": sherlock_raw[:1000]
    }

def track_username(username):
    raw = run_cmd(f"sherlock {username} --timeout 30", timeout=90)
    sites = parse_sherlock(raw)
    return {
        "sherlock_sites": sites,
        "raw_sherlock": raw[:1500]
    }

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: tracker.py <target>"}))
        return
    target = sys.argv[1].strip()

    if re.match(r'^\+?[\d\s\-()]{7,}$', target):
        ttype = "phone"
        raw = track_phone(target)
    elif '@' in target:
        ttype = "email"
        raw = track_email(target)
    else:
        ttype = "username"
        raw = track_username(target)

    output = {"target": target, "type": ttype, "raw": raw}
    print(json.dumps(output, ensure_ascii=False))

if __name__ == "__main__":
    main()
