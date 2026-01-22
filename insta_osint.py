import os
import sys
import time
import instaloader
from colorama import Fore, Style, init

init(autoreset=True)

# ================= EFFECTS =================

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def typing(text, color=Fore.GREEN, speed=0.03):
    for c in text:
        sys.stdout.write(color + c)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# ================= UI =================

def banner():
    print(Fore.GREEN + r"""
 ██████╗ ███████╗██╗███╗   ██╗████████╗   ██╗ ██████╗ 
██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝   ██║██╔════╝ 
██║   ██║███████╗██║██╔██╗ ██║   ██║█████╗██║██║  ███╗
██║   ██║╚════██║██║██║╚██╗██║   ██║╚════╝██║██║   ██║
╚██████╔╝███████║██║██║ ╚████║   ██║      ██║╚██████╔╝
 ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝      ╚═╝ ╚═════╝
""")
    print(Fore.CYAN + " Tool   : osint.ig")
    print(Fore.CYAN + " Author : ionutivan21\n")

def menu():
    print(Fore.GREEN + """
[1] Profile information
[2] Download ALL public posts
[3] Bio OSINT (emails / links)
[4] Posts timeline (dates)
[0] Exit
""")

# ================= CORE =================

def load_profile(username):
    L = instaloader.Instaloader(quiet=True)
    try:
        return instaloader.Profile.from_username(L.context, username)
    except:
        typing("[!] Failed to load profile (rate-limit or wrong username)", Fore.RED)
        sys.exit()

def show_info(p):
    typing("\n[+] PROFILE INFORMATION\n", Fore.CYAN)
    typing(f"Name       : {p.full_name}")
    typing(f"Username   : {p.username}")
    typing(f"Bio        : {p.biography}")
    typing(f"Followers : {p.followers}")
    typing(f"Following : {p.followees}")
    typing(f"Posts     : {p.mediacount}")
    typing(f"Website   : {p.external_url}")
    typing(f"Private   : {p.is_private}")

def download_posts(p):
    if p.is_private:
        typing("[!] Account is private. Posts not public.", Fore.RED)
        return

    base = os.path.join(os.getcwd(), f"{p.username}_posts")
    os.makedirs(base, exist_ok=True)

    L = instaloader.Instaloader(
        download_pictures=True,
        download_videos=True,
        download_video_thumbnails=False,
        save_metadata=False,
        dirname_pattern=base,
        quiet=True
    )

    typing("\n[+] Downloading public posts...\n", Fore.CYAN)
    L.download_profile(p.username, profile_pic=False)
    typing("\n[✓] Download complete", Fore.GREEN)

def bio_osint(p):
    typing("\n[+] BIO OSINT\n", Fore.CYAN)
    found = False

    for word in p.biography.split():
        if "@" in word and "." in word:
            typing(f"[EMAIL] {word}", Fore.GREEN)
            found = True
        if word.startswith("http"):
            typing(f"[LINK] {word}", Fore.GREEN)
            found = True

    if not found:
        typing("[!] Nothing interesting found", Fore.YELLOW)

def timeline(p):
    typing("\n[+] POSTS TIMELINE (latest 10)\n", Fore.CYAN)
    for i, post in enumerate(p.get_posts(), 1):
        typing(f"{i}. {post.date_utc} | Likes: {post.likes}")
        if i == 10:
            break

# ================= MAIN =================

def main():
    clear()
    banner()

    typing("Enter Instagram username: ", Fore.GREEN, 0.02)
    username = input().strip()

    typing("\n[*] Loading profile...\n", Fore.YELLOW, 0.02)
    profile = load_profile(username)

    while True:
        menu()
        choice = input(Fore.GREEN + "Select option > ").strip()

        if choice == "1":
            show_info(profile)
        elif choice == "2":
            download_posts(profile)
        elif choice == "3":
            bio_osint(profile)
        elif choice == "4":
            timeline(profile)
        elif choice == "0":
            typing("\n[+] Exit\n", Fore.RED)
            break
        else:
            typing("[!] Invalid option", Fore.RED)

        input(Fore.CYAN + "\nPress ENTER to continue...")
        clear()
        banner()

if __name__ == "__main__":
    main()
