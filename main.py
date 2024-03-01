import cloudscraper, base64, requests, webview, time, os, subprocess
from lxml import html

version = 0.1
base = "https://fr.coflix.nu/"
ascii = requests.get("https://paste.ee/r/ZhGGS").text # This make the code shorter

class Scraper:
    def __init__(self, query):
        self.query = query

    def search(self):
        scraper = cloudscraper.create_scraper()
        tree = html.fromstring(scraper.get(f"{base}?s={self.query}").content)
        results = tree.xpath('//*[@id="results"]/div[@class="bx por"]')
        search_results = []
        for result in results:
            name = result.xpath('.//div[@class="ttl link-co fwb fz14"]/text()')[0].strip()
            uuid = result.get("data-uuid")
            search_results.append({"name": name, "id": uuid})
        return search_results


class Watch:
    def __init__(self, id, type="movie"):
        self.id = id
        self.type = type

    def links(self, episode=None):
        episode = 1 if self.type == "serie" and episode == None else None
        scraper = cloudscraper.create_scraper(browser='chrome')
        t = html.fromstring(scraper.get(f"{base}?trembed=0&trid={self.id}&trtype=1").content) if self.type == "movie" else html.fromstring(scraper.get(f"{base}?trembed=0&trid={self.id}&trtype=2&vr={episode}").content)
        tree = html.fromstring(scraper.get(f"{t.xpath('//iframe')[0].get('src')}").content)
        onclick_elements = tree.xpath('//*/@onclick[starts-with(., "showVideo")]')
        video_urls = [base64.b64decode(element.split('\'')[1]).decode('utf-8') for element in onclick_elements]
        return video_urls

def center(var:str, space:int=None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

def link(l):
    return True if requests.get(l).status_code == 200 else False

def menu():
    os.system("cls && title PyFlix 0.1 - github.com/vodkarm/PyFlix")
    print("\033[1;35;40m" + center(ascii) + "\033[m")
    print("\n"*3)
    t = input(f"Will you watch a movie or a serie [m/s] >> ")
    query = input(f"Enter a movie name >> ") if t == "m" else input(f"Enter a serie name >> ")
    s = Scraper(query).search()
    if s == []:
        print("Not Found!")
        time.sleep(3)
        menu()
    else:
        pass
    for i, result in enumerate(s):
        print(f"[{i+1}] {result['name']}")
    c = int(input("Please enter the number corresponding to the desired movie >> ")) if t == "m" else int(input("Please enter the number corresponding to the desired serie >> "))
    links = Watch(s[c]["id"], "movie" if t == "m" else "serie").links(None if t == "m" else int(input("Please enter the episode number >> ")))
    for l in links:
        if link(l):
            webview.create_window(f'PyFlix - {s[c]["name"]} - Good watching!', l)
            webview.start()
            break
        else:
            continue
    menu()

menu()
