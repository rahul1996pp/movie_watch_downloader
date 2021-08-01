from os.path import dirname, realpath
from os import system
from requests import get
from tabulate import tabulate
from colorama import Fore, init, Style

bright = Style.BRIGHT
green, blue, red, cyan, reset = Fore.GREEN + bright, Fore.BLUE + bright, Fore.RED + bright, Fore.CYAN, Fore.RESET
init(convert=True, autoreset=True)

def process():
    global data_json, data_list, data_menu, mov_name
    mov_name = input("[+] Enter movie name: ")
    payload['query_term'] = mov_name
    data = get(url, params=payload)
    data_json = data.json()
    data_list = {'movie_url': [], 'torrent_url': []}
    data_menu = {'sl.no': [], 'movie_title': [], 'movie_year': [], 'quality': [], 'type': [], 'seeds': [], 'size': []}
    if movie_list():
        print(tabulate(data_menu, headers=['sl.no', 'movie_title', 'movie_year', 'quality', 'type', 'seeds', 'size'],tablefmt='pretty'))
        choice = int(input("[+] select your movie :- ")) - 1
        print(f"[+] movie name :- {data_menu['movie_title'][choice]} --> {data_list['torrent_url'][choice]} --> {data_menu['size'][choice]}")
        video_watch(data_list['torrent_url'][choice])


def movie_list():
    if data_json["data"]['movie_count'] > 0 and len(mov_name) > 0:
        num = 0
        for s in range(len(data_json['data']['movies'])):
            for j in range(len(data_json['data']['movies'][s]['torrents'])):
                data_list['movie_url'].append(data_json['data']['movies'][s]['url'])
                data_list['torrent_url'].append(data_json['data']['movies'][s]['torrents'][j]['url'])
                num += 1
                data_menu['sl.no'].append(num)
                data_menu['movie_title'].append(data_json['data']['movies'][s]['title'])
                data_menu['movie_year'].append(data_json['data']['movies'][s]['year'])
                data_menu['quality'].append(data_json['data']['movies'][s]['torrents'][j]['quality'])
                data_menu['type'].append(data_json['data']['movies'][s]['torrents'][j]['type'])
                data_menu['seeds'].append(data_json['data']['movies'][s]['torrents'][j]['seeds'])
                data_menu['size'].append(data_json['data']['movies'][s]['torrents'][j]['size'])
        return True
    else:
        print(f"{red}[-] no movie found")
        return False


def video_watch(torrent_url):
    credit()
    base_dir = dirname(realpath(__file__))
    node_exe = base_dir + r'\movie\Scripts\node.exe'
    app_js = base_dir + r'\movie\Scripts\node_modules\peerflix\app.js'
    url = f'{node_exe} {app_js} {torrent_url} -c 1000 --vlc'
    system(f"start cmd /k {url}")


def credit():
    credit_text = f"""
               {red}YIFY MOVIE STREAMER
{green}               
     ██▀███   ▄▄▄       ██░ ██  █    ██  ██▓    
    ▓██ ▒ ██▒▒████▄    ▓██░ ██▒ ██  ▓██▒▓██▒    
    ▓██ ░▄█ ▒▒██  ▀█▄  ▒██▀▀██░▓██  ▒██░▒██░    
    ▒██▀▀█▄  ░██▄▄▄▄██ ░▓█ ░██ ▓▓█  ░██░▒██░    
    ░██▓ ▒██▒ ▓█   ▓██▒░▓█▒░██▓▒▒█████▓ ░██████▒
    ░ ▒▓ ░▒▓░ ▒▒   ▓▒█░ ▒ ░░▒░▒░▒▓▒ ▒ ▒ ░ ▒░▓  ░
      ░▒ ░ ▒░  ▒   ▒▒ ░ ▒ ░▒░ ░░░▒░ ░ ░ ░ ░ ▒  ░
      ░░   ░   ░   ▒    ░  ░░ ░ ░░░ ░ ░   ░ ░   
       ░           ░  ░ ░  ░  ░   ░         ░  ░ {blue}code generated by Rahul.p\n
    """
    print(credit_text)


url = "https://yts.mx/api/v2/list_movies.json"
payload = {}
credit()
process()
