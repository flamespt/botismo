import random, time, requests, threading
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from bs4 import BeautifulSoup
browser_def = 'multiple_browsers.txt'
def import_browser_def():
    browsers = []
    with open(browser_def,'rb') as ficheiro:
        for linhas in ficheiro.readlines():
            browsers.append(linhas.strip().decode('utf8'))
    return browsers

browser = import_browser_def()

def proxies():
    address = []
    response = requests.get('https://www.sslproxies.org/')
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.findAll("tr")
    for row in rows:
        if (len(row.findAll("td"))==8):
            address.append((row.contents[0].contents[0] + ':' +row.contents[1].contents[0]))
    return random.choice(address)


def drivers():
    while (True):
        # proxies()

        PROXY = proxies()

        proxy_ip = PROXY.split(":")[0]
        proxy_port = PROXY.split(":")[1]

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': PROXY,
            'ftpProxy': PROXY,
            'sslProxy': PROXY,
            'noProxy': ''
        })
        profile = webdriver.FirefoxProfile();
        profile.set_preference('general.useragent.override', random.choice(browser))
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.share_proxy_settings", True)
        profile.set_preference("network.http.use-cache", False)
        profile.set_preference("network.proxy.http", proxy_ip)
        profile.set_preference("network.proxy.http_port", int(proxy_port))
        profile.set_preference('network.proxy.ssl_port', int(proxy_port))
        profile.set_preference('network.proxy.ssl', proxy_ip)
        profile.set_preference('network.proxy.socks', proxy_ip)
        profile.set_preference('network.proxy.socks_port', int(proxy_port))
        profile.update_preferences()
        driver = webdriver.Firefox(firefox_profile=profile, proxy=proxy)

        try:
            driver.get('https://www.youtube.com/watch?v=VvbhHYQqU1c')
            time.sleep(random.randint(60,120))
            driver.quit()
            break;
        except:
            driver.quit()
        # sair = input("Deseja sair?")
        # if sair == 'sim':
        #     driver.quit()
        #     break
        # else:
        #     driver.quit()

if __name__ == "__main__":
    for i in range(3):
        t = threading.Thread(target=drivers)
        t.start()


    #for i in range(2):

      #  print(random.choice(browser))