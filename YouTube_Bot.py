from selenium import webdriver
import random, time, threading, colorama, os, requests, sys
from colorama import Fore
from pathlib import Path
colorama.init()
def banner():
    return rf"""{Fore.CYAN}
     __      ___                          ___    ___  
     \ \    / (_)                        |__ \  / _ \ 
      \ \  / / _  _____      _____ _ __     ) || | | |
       \ \/ / | |/ _ \ \ /\ / / _ \ '__|   / / | | | |
        \  /  | |  __/\ V  V /  __/ |     / /_ | |_| |
         \/   |_|\___| \_/\_/ \___|_|    |____(_)___/ 
                {Fore.LIGHTRED_EX}© Copyright by LukeProducts
    {Fore.RESET}                                                                                                                       
    """
def instruction():
    return f"""{Fore.LIGHTMAGENTA_EX}Hey there! This is the advanced viewer bot working with proxys.
Please understand that You must give this program time to work.{Fore.RESET}
"""
def check_valid_URL(url):
    try:
        requests.get(url)
        return True
    except:
        return False
def traffic(url, proxylist, min_watchtime, max_watchtime, views_per_thread, mute, browser):
    if browser == "Firefox" or browser == "firefox":
        for proxy in proxylist:
            ip, port = proxy.split(':')
            opts = webdriver.FirefoxProfile()
            opts.set_preference("network.proxy.type", 1)
            opts.set_preference("network.proxy.socks", ip)
            opts.set_preference("network.proxy.socks_port", int(port))
            opts.set_preference("network.proxy.socks_version", 4)
            opts.update_preferences()
            if mute:
                opts.set_preference('media.volume_scale', "0.0")
                opts.update_preferences()
            driver = webdriver.Firefox(executable_path="libs/drivers/geckodriver.exe", firefox_profile=opts)
            try:
                driver.get(url)
                print(f"Using: {proxy}")
                driver.find_element_by_xpath('//*[@id="movie_player"]/div[27]/div[2]/div[1]/button').click()
            except:
                driver.close()
                continue
            for session in range(views_per_thread):
                time.sleep(random.randint(min_watchtime, max_watchtime))
                driver.refresh()
                driver.find_element_by_xpath('//*[@id="movie_player"]/div[27]/div[2]/div[1]/button').click()
            driver.quit()
            return True
    elif browser == "Chrome" or browser == "chrome":
        url += "?autoplay=1"
        for i in range(50):
            proxy = random.choice(proxylist)

            opts = webdriver.ChromeOptions()
            opts.add_argument('--proxy-server=socks4://' + proxy)

            driver = webdriver.Chrome("libs/drivers/chromedriver.exe", options=opts)
            try:
                driver.get(url)
                print(f"Using: {proxy}")
            except:
                driver.close()
                continue
            for session in range(views_per_thread):
                time.sleep(random.randint(min_watchtime, max_watchtime))
                driver.refresh()
            driver.close()
def thread_start_traffic(url, proxylist, min_watchtime, max_watchtime, views_per_thread, mute, threads, browser):
    print("processing... [check your statistics]")
    for Thread in range(threads):
        threading.Thread(target=traffic, args=(url, proxylist, min_watchtime, max_watchtime, views_per_thread, mute, browser)).start()
    return True

try:
    while True:
        os.system('cls')
        print(banner())
        #setup
        if not Path("libs").is_dir():
            print(f"{Fore.RED}directory 'libs' does not exist{Fore.RESET}")
            break
        try:
            with open("libs/proxys/socks4.txt") as f:
                socks4proxylist = f.read().split('\n')
        except:
            print(f"{Fore.RED}file 'socks4.txt' not in libs/proxys/ folder!{Fore.RESET}")
            break
        if socks4proxylist == []:
            print(f"{Fore.RED}No proxys loaded!{Fore.RESET}")
            break
        if not Path("libs/drivers/geckodriver.exe").is_file():
            print(f"{Fore.RED}file 'geckobdriver.exe' not in libs/drivers/ folder!{Fore.RESET}")
            break
        if not Path("libs/drivers/chromedriver.exe").is_file():
            print(f"{Fore.RED}file 'chromedriver.exe' not in libs/drivers/ folder!{Fore.RESET}")
            break
        #setup
        print(instruction())
        URL = input("Enter video URL here:\n>> ")
        if not check_valid_URL(URL):
            print(f"{Fore.RED}No reachable URL given!{Fore.RESET}")
            time.sleep(1)
            continue
        print(f"[{Fore.GREEN}>{Fore.RESET}] URL: {Fore.GREEN}{URL}{Fore.RESET}")
        try:
            min_watchtime = int(input("Enter minimum watchtime here:\n>> "))
            print(f"[{Fore.GREEN}>{Fore.RESET}] min. watchtime set to: {Fore.GREEN}{min_watchtime}{Fore.RESET}")
        except:
            print(f"{Fore.RED}No integer was entered!{Fore.RESET}")
            time.sleep(1)
            continue
        try:
            max_watchtime = int(input("Enter maximum watchtime here:\n>> "))
            print(f"[{Fore.GREEN}>{Fore.RESET}] max. watchtime set to: {Fore.GREEN}{max_watchtime}{Fore.RESET}")
        except:
            print(f"{Fore.RED}No integer was entered!{Fore.RESET}")
            time.sleep(1)
            continue
        try:
            threads = int(input("Enter threads to use [WARNING: multiple threads can cause crashes and a high processor load]\n>> "))
            print(f"[{Fore.GREEN}>{Fore.RESET}] threads set to {Fore.GREEN}{threads}{Fore.RESET}")
        except:
            print(f"{Fore.RED}No integer was entered!{Fore.RESET}")
            time.sleep(1)
            continue
        try:
            views_per_thread = int(input("Enter Views per proxy thread: [max. 10 recommended]\n>> "))
            print(f"[{Fore.GREEN}>{Fore.RESET}] views per thread set to {Fore.GREEN}{views_per_thread}{Fore.RESET}")
        except:
            print(f"{Fore.RED}No integer was entered!{Fore.RESET}")
            continue
        mute_autio = input("Shall the browser audio be muted? [Yes: Y / No: N]\n>>")
        if mute_autio == "y" or mute_autio == "Y":
            mute_autio = True
        elif mute_autio == 'n' or mute_autio == 'N':
            mute_autio = False

        else:
            print(f"{Fore.RED}No valid option!{Fore.RESET}")
            time.sleep(1)
            continue
        print(f"browser muting status: {Fore.GREEN}{mute_autio}")

        try:
            print(f"Decide which browser to use: {Fore.GREEN}[1]{Fore.RESET}Chrome {Fore.RED}[2]{Fore.RESET}Firefox")
            browser = int(input(">> "))
            if browser == 1:
                browser = "Chrome"
            elif browser == 2:
                browser = "Firefox"
            print(f"[{Fore.GREEN}>{Fore.RESET}] browser set to {Fore.LIGHTGREEN_EX}{browser}{Fore.RESET}")
        except:
            print(f"{Fore.RED}No valid argument given!{Fore.RESET}")
            continue
        thread_start_traffic(URL, socks4proxylist, min_watchtime, max_watchtime, views_per_thread, mute_autio, threads, browser)
        break
except KeyboardInterrupt:
    print(f"\n{Fore.RED}exiting...{Fore.RESET}")
