from selenium import webdriver
import random, time, threading
from pathlib import Path
def banner():
    return r"""
     __      ___                          ___    ___  
     \ \    / (_)                        |__ \  / _ \ 
      \ \  / / _  _____      _____ _ __     ) || | | |
       \ \/ / | |/ _ \ \ /\ / / _ \ '__|   / / | | | |
        \  /  | |  __/\ V  V /  __/ |     / /_ | |_| |
         \/   |_|\___| \_/\_/ \___|_|    |____(_)___/ 
               © Copyright by LukeProducts                                                                                                      
    """
def instruction():
    return """Hey there! This is the advanced viewer bot working with proxys.
Please understand that You must give this program time to work
"""
def traffic(url, proxylist, min_watchtime, max_watchtime, views_per_thread, mute):
    for proxy in proxylist:
        ip, port = proxy.split(':')
        browser = webdriver.FirefoxProfile()
        browser.set_preference("network.proxy.type", 1)
        browser.set_preference("network.proxy.socks", ip)
        browser.set_preference("network.proxy.socks_port", int(port))
        browser.set_preference("network.proxy.socks_version", 4)
        browser.update_preferences()
        if mute:
            browser.set_preference('media.volume_scale', "0.0")
            browser.update_preferences()
        driver = webdriver.Firefox(executable_path="libs/geckodriver.exe", firefox_profile=browser)
        try:
            driver.get(url)
            driver.find_element_by_xpath('//*[@id="movie_player"]/div[27]/div[2]/div[1]/button').click()
        except:
            continue
        for session in range(views_per_thread):
            time.sleep(random.randint(min_watchtime, max_watchtime))
            driver.refresh()
        driver.quit()
        return True
def thread_start_traffic(url, proxylist, min_watchtime, max_watchtime, views_per_thread, mute, threads):
    print("processing... [check your statistics]")
    for Thread in range(threads):
        threading.Thread(target=traffic, args=(url, proxylist, min_watchtime, max_watchtime, views_per_thread, mute)).start()
    return True
while True:
    print(banner())
    print(instruction())
    URL = input("Enter video URL here:\n>> ")
    URL += "?autoplay=1"
    try:
        min_watchtime = int(input("Enter minimum watchtime here:\n>> "))
    except:
        print("No integer was entered!")
        continue
    try:
        max_watchtime = int(input("Enter maximum watchtime here:\n>> "))
    except:
        print("No integer was entered!")
        continue
    try:
        threads = int(input("Enter threads to use [WARNING: multiple threads can cause crashes and a high processor load]\n>> "))
    except:
        print("No valid integer given!")
        continue
    try:
        views_per_thread = int(input("Enter Views per proxy thread: [max. 10 recommended]\n>> "))
    except:
        print("No integer was entered!")
        continue
    mute_autio = input("Shall the browser audio be muted? [Yes: Y / No: N]\n>>")
    if mute_autio == "y" or mute_autio == "Y":
        mute_autio = True
    elif mute_autio == 'n' or mute_autio == 'N':
        mute_autio = False
    else:
        print("No valid option!")
        continue
    if not Path("libs").is_dir():
        print("directory 'libs' does not exist")
        break
    try:
        with open("libs/socks4.txt") as f:
            socks4proxylist = f.read().split('\n')
    except:
        print("file 'socks4.txt' not in libs folder!")
        break
    if socks4proxylist == []:
        print("No proxys loaded!")
        break

    if not Path("libs/geckodriver.exe").is_file():
        print("file 'geckobdriver.exe' not in libs folder!")
        break
    try:
        proxy_usage = int(input(f"Enter amount of proxys being used: [max. {len(socks4proxylist) - 1}]\n>> "))
        if proxy_usage > (len(socks4proxylist) - 1):
            print(f"there are not {proxy_usage} proxys loaded, choosing maximum of {len(socks4proxylist) - 1}")
            proxy_usage = len(socks4proxylist) - 1
        print(f"proxys using: {proxy_usage}")
    except:
        print("No valid amount of proxies!")
        break
    thread_start_traffic(URL, socks4proxylist[0:proxy_usage], min_watchtime, max_watchtime, views_per_thread, mute_autio, threads)
    print(f"optimal view amount of {threads * views_per_thread} is getting generated!")
    break
