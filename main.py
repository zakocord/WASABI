import requests
import os
import time
import json
from pystyle import *
from colorama import *

init(autoreset=True)

ascii_art = """
                                ██╗    ██╗ █████╗ ███████╗ █████╗ ██████╗ ██╗
                                ██║    ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║
                                ██║ █╗ ██║███████║███████╗███████║██████╔╝██║
                                ██║███╗██║██╔══██║╚════██║██╔══██║██╔══██╗██║
                                ╚███╔███╔╝██║  ██║███████║██║  ██║██████╔╝██║
                                 ╚══╝╚══╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝
                                            [1]. Token Checker
                                            [2]. Start Advertising
                                            [3]. Guild Checker
[!]. Config
[?]. Credit
"""

with open("tokens.txt", "r", encoding="utf-8") as file:
    tokens = file.readlines()

with open("config.json", "r", encoding="utf-8") as file:
        configs = json.load(file)

def guild_checker(tokens):
    guild_id = Write.Input("@WASABI~@Guild-Checker: ", Colors.green_to_yellow, interval=0.0000)

    for token in tokens:
        token = token.strip()
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        response = requests.get("https://discord.com/api/v9/users/@me/guilds", headers=headers)

        if response.status_code == 200:
            guilds = response.json()
            in_guild = any(g["id"] == guild_id for g in guilds)

            if in_guild:
                print(f"{Fore.GREEN}[+] {Fore.RESET}{token} {Fore.GREEN}Joined")
            else:
                print(f"{Fore.RED}[-] {Fore.RESET}{token} {Fore.RED}Not Joined")

        elif response.status_code == 401:
            print(f"{Fore.RED}[-] {Fore.RESET}{token} {Fore.RED}Invalid")
        else:
            print(f"{Fore.RED}[-] ERROR")

def check_token(tokens):
    for token in tokens:
        token = token.strip()
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

        if response.status_code == 200:
            with open("valid.txt", "a", encoding="utf-8") as f:
                f.write(token + "\n")
            print(f"{Fore.GREEN}[+] {Fore.RESET}{token} {Fore.GREEN}Valid")
        
        elif response.status_code == 401:
            with open("invalid.txt", "a", encoding="utf-8") as f:
                f.write(token + "\n")
            print(f"{Fore.RED}[-] {Fore.RESET}{token} {Fore.RED}Invalid")
        
        else:
            print(f"{Fore.YELLOW}[!] {Fore.RESET}{token} Error: {response.status_code}")

def send(config):
    channels = config["channel"]
    message = config["message"]

    print(f"{Fore.GREEN} Start The Advertising. [Ctrl+C to Exit]")

    for token in tokens:  # Loop through tokens
        headers = {
            "Authorization": token.strip(),
            "Content-Type": "application/json"
        }
        while True:
            for channel_id in channels:
                try:
                    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
                    payload = {"content": message}
                    response = requests.post(url, headers=headers, json=payload)

                    if response.status_code == 200 or response.status_code == 204:
                        print(f"{Fore.GREEN}[+] {channel_id} Sent")

                    elif response.status_code == 429:
                        retry_after = response.json().get("retry_after", 5)
                        print(f"{Fore.YELLOW}[!] Ratelimit {channel_id} | {retry_after}s")
                        time.sleep(retry_after)

                    elif response.status_code == 401:
                        print(f"{Fore.YELLOW}[!] Unauthorized")

                    elif "You are sending messages too quickly" in response.text:
                        print(f"{Fore.YELLOW}[!] Slow Mode {channel_id}")
                        time.sleep(10)

                    else:
                        print(f"{Fore.RED}[-] ERROR | {response.status_code} - {response.text}")
                        time.sleep(5)

                except Exception as e:
                    print(f"{Fore.RED}[!] Exception: {e}")
                    time.sleep(5)

def main():
    print(Colorate.Horizontal(Colors.green_to_yellow, ascii_art, 1))
    print(" ")
    print(" ")
    print(" ")
    choice = Write.Input("@WASABI~@Home: ", Colors.green_to_yellow, interval=0.0000)

    if choice == "1":
        check_token(tokens)
        os.system("pause")
        os.system("cls")
        main()
    if choice == "2":
        send(configs)
        os.system("pause")
        os.system("cls")
        main()
    if choice == "3":
        guild_checker(tokens)
        os.system("pause")
        os.system("cls")
        main()

if __name__ == "__main__":
    main()
