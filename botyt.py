import random, time, requests
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

if __name__ == "__main__":


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

        driver = webdriver.Firefox(firefox_profile=profile, proxy=proxy)
        driver.get('https://www.ipchicken.com/')
        sair = input("Deseja sair?")
        if sair == 'sim':
            driver.quit()
            break
        else:
            driver.quit()

    #for i in range(2):

      #  print(random.choice(browser))