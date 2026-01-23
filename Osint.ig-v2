#!/usr/bin/env python3
# osint.ig | Instagram OSINT Tool - FINAL
# Author: ionutivan21

import os, sys, time, json, csv, zipfile, hashlib
from datetime import datetime
import instaloader
from colorama import Fore, init
from fpdf import FPDF

init(autoreset=True)

BASE = "/storage/emulated/0/Pictures/osint.ig"
CFG_FILE = "config.json"

DEFAULT_CFG = {
  "typing_speed": 0.01,
  "fast_delay": 0.4,
  "stealth_delay": 2.0,
  "max_hashtags": 40
}

# ---------------- CONFIG ----------------
def load_cfg():
    if not os.path.exists(CFG_FILE):
        with open(CFG_FILE,"w") as f: json.dump(DEFAULT_CFG,f,indent=2)
    with open(CFG_FILE) as f: return json.load(f)

CFG = load_cfg()

# ---------------- UI ----------------
def clear(): os.system("clear")
def typing(t,c=Fore.GREEN):
    for x in t:
        sys.stdout.write(c+x); sys.stdout.flush()
        time.sleep(CFG["typing_speed"])
    print()

def banner():
    print(Fore.GREEN + r"""
 ██████╗ ███████╗██╗███╗   ██╗████████╗   ██╗ ██████╗ 
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝   ██║██╔════╝ 
██║   ██║███████╗██║██╔██╗ ██║   ██║█████╗██║██║  ███╗
██║   ██║╚════██║██║██║╚██╗██║   ██║╚════╝██║██║   ██║
╚██████╔╝███████║██║██║ ╚████║   ██║      ██║╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝ ╚═════╝
""")
    print(Fore.CYAN+"osint.ig | FINAL | Author: ionutivan21\n")

def menu():
    print(Fore.GREEN+"""
[01] Profile information
[02] Download ALL posts (FAST)
[03] Download ALL posts (STEALTH)
[04] Download ONLY images
[05] Download ONLY videos
[06] Download REELS
[07] Download captions (.txt)
[08] Bio OSINT (emails / links)
[09] Hashtag intelligence (top)
[10] Posts timeline (CSV)
[11] Generate TXT report
[12] Generate PDF report
[13] Export JSON report
[14] Export CSV (posts stats)
[15] Scan MULTI usernames (list)
[16] ZIP export (all data)
[17] Clear cache (user)
[18] Open gallery folder
[19] Settings (config.json)
[20] Check username exists
[00] Exit
""")

# ---------------- CORE ----------------
def dirs(u):
    p=f"{BASE}/{u}"
    for d in ["images","videos","reels","captions","reports","cache","csv"]:
        os.makedirs(f"{p}/{d}",exist_ok=True)
    return p

def loader(u):
    L=instaloader.Instaloader(quiet=True)
    return instaloader.Profile.from_username(L.context,u)

def scan(path): os.system(f"termux-media-scan {path}")

def cache_hit(path, key):
    h=hashlib.md5(key.encode()).hexdigest()
    f=f"{path}/cache/{h}"
    if os.path.exists(f): return True
    open(f,"w").close(); return False

# ---------------- FEATURES ----------------
def info(p):
    typing(f"Username : {p.username}")
    typing(f"Name     : {p.full_name}")
    typing(f"Followers: {p.followers}")
    typing(f"Following: {p.followees}")
    typing(f"Posts    : {p.mediacount}")
    typing(f"Private  : {p.is_private}")
    typing(f"Bio      : {p.biography}")

def download_posts(p,mode="all",delay=0.5):
    if p.is_private: typing("[!] Private",Fore.RED); return
    path=dirs(p.username); L=instaloader.Instaloader(quiet=True)
    for post in p.get_posts():
        if cache_hit(path,post.shortcode): continue
        if mode=="images" and post.is_video: continue
        if mode=="videos" and not post.is_video: continue
        target="videos" if post.is_video else "images"
        if mode=="reels": target="reels"
        L.download_post(post,f"{path}/{target}")
        if post.caption:
            with open(f"{path}/captions/{post.shortcode}.txt","w",encoding="utf-8") as f:
                f.write(post.caption)
        time.sleep(delay)
    scan(path); typing("[✓] Saved to Gallery",Fore.GREEN)

def captions_only(p):
    path=dirs(p.username)
    for post in p.get_posts():
        if post.caption:
            with open(f"{path}/captions/{post.shortcode}.txt","w",encoding="utf-8") as f:
                f.write(post.caption)
    typing("[✓] Captions saved",Fore.GREEN)

def bio_osint(p):
    for w in p.biography.split():
        if "@" in w or "http" in w: typing(w,Fore.CYAN)

def hashtags(p):
    tags={}
    for post in p.get_posts():
        if post.caption:
            for w in post.caption.split():
                if w.startswith("#"):
                    tags[w.lower()]=tags.get(w.lower(),0)+1
    for h,c in sorted(tags.items(), key=lambda x:x[1], reverse=True)[:CFG["max_hashtags"]]:
        typing(f"{h} ({c})",Fore.CYAN)

def timeline_csv(p):
    path=dirs(p.username)
    out=f"{path}/csv/timeline.csv"
    with open(out,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["date","likes","comments"])
        for post in p.get_posts():
            w.writerow([post.date.strftime("%Y-%m-%d"),post.likes,post.comments])
    typing("[✓] CSV timeline created",Fore.GREEN)

def txt_report(p):
    path=f"{BASE}/{p.username}/reports/report.txt"
    with open(path,"w",encoding="utf-8") as f: f.write(str(p._asdict()))
    typing("[✓] TXT report",Fore.GREEN)

def pdf_report(p):
    path=f"{BASE}/{p.username}/reports/report.pdf"
    pdf=FPDF(); pdf.add_page(); pdf.set_font("Arial","",11)
    for k,v in p._asdict().items(): pdf.multi_cell(0,8,f"{k}: {v}")
    pdf.output(path); typing("[✓] PDF report",Fore.GREEN)

def json_report(p):
    path=f"{BASE}/{p.username}/reports/report.json"
    with open(path,"w",encoding="utf-8") as f: json.dump(p._asdict(),f,indent=2)
    typing("[✓] JSON exported",Fore.GREEN)

def csv_posts(p):
    path=dirs(p.username)
    out=f"{path}/csv/posts.csv"
    with open(out,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["shortcode","date","likes","comments","is_video"])
        for post in p.get_posts():
            w.writerow([post.shortcode,post.date_utc,post.likes,post.comments,post.is_video])
    typing("[✓] Posts CSV exported",Fore.GREEN)

def scan_multi():
    file=input("List file (usernames.txt) > ").strip()
    if not os.path.exists(file): typing("File not found",Fore.RED); return
    with open(file) as f:
        for u in [x.strip() for x in f if x.strip()]:
            try:
                p=loader(u); dirs(u)
                typing(f"[✓] {u} OK",Fore.GREEN)
            except:
                typing(f"[!] {u} FAIL",Fore.RED)

def zip_export(u):
    src=f"{BASE}/{u}"
    z=f"{BASE}/{u}/{u}_export.zip"
    with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zipf:
        for root,_,files in os.walk(src):
            for file in files:
                fp=os.path.join(root,file)
                zipf.write(fp, fp.replace(src,""))
    typing("[✓] ZIP created",Fore.GREEN)

def open_gallery(u): os.system(f"xdg-open {BASE}/{u}")
def check_user(u):
    try: loader(u); typing("[✓] Exists",Fore.GREEN)
    except: typing("[!] Invalid / blocked",Fore.RED)

# ---------------- MAIN ----------------
def main():
    clear(); banner()
    u=input(Fore.GREEN+"Username > ").strip()
    try: p=loader(u)
    except: typing("Cannot load",Fore.RED); return
    dirs(u)

    while True:
        menu()
        c=input(Fore.GREEN+"> ").strip()
        if c=="01": info(p)
        elif c=="02": download_posts(p,"all",CFG["fast_delay"])
        elif c=="03": download_posts(p,"all",CFG["stealth_delay"])
        elif c=="04": download_posts(p,"images",CFG["fast_delay"])
        elif c=="05": download_posts(p,"videos",CFG["fast_delay"])
        elif c=="06": download_posts(p,"reels",1.0)
        elif c=="07": captions_only(p)
        elif c=="08": bio_osint(p)
        elif c=="09": hashtags(p)
        elif c=="10": timeline_csv(p)
        elif c=="11": txt_report(p)
        elif c=="12": pdf_report(p)
        elif c=="13": json_report(p)
        elif c=="14": csv_posts(p)
        elif c=="15": scan_multi()
        elif c=="16": zip_export(u)
        elif c=="17": os.system(f"rm -rf {BASE}/{u}/cache")
        elif c=="18": open_gallery(u)
        elif c=="19": typing("Edit config.json",Fore.YELLOW)
        elif c=="20": check_user(u)
        elif c=="00": break
        else: typing("Invalid",Fore.RED)
        input(Fore.CYAN+"\nENTER...")
        clear(); banner()

if __name__=="__main__": main()
