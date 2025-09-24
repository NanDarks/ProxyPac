import requests
import re

# List of proxy sources in RAW format
# This list now focuses ONLY on HTTPS and SOCKS5 proxies.
PROXY_SOURCES = [
    'https://raw.githubusercontent.com/mmpx12/proxy-list/main/socks5/http.txt',
    'https://raw.githubusercontent.com/noctiro/getproxy/master/file/socks5.txt',
]

def get_proxies_from_sources(sources):
    """Fetches and combines proxies from a list of URLs."""
    all_proxies = set()
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                proxies = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+', response.text)
                for proxy in proxies:
                    all_proxies.add(proxy)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching proxies from {url}: {e}")
    return all_proxies

def check_proxy(proxy):
    """Checks if a proxy is working by connecting to a test URL."""
    proxies = {'http': f'http://{proxy}', 'https': f'https://{proxy}'}
    try:
        requests.get('https://www.google.com', proxies=proxies, timeout=10)
        return True
    except requests.exceptions.RequestException:
        return False

def main():
    print("Fetching proxy lists...")
    all_proxies = get_proxies_from_sources(PROXY_SOURCES)
    print(f"Found {len(all_proxies)} proxies to check.")
    
    working_proxies = []
    for i, proxy in enumerate(all_proxies):
        print(f"Checking proxy {i+1}/{len(all_proxies)}: {proxy}")
        if check_proxy(proxy):
            working_proxies.append(proxy)
            print("  --> Working!")
        else:
            print("  --> Not working.")
            
    with open('working_proxies.txt', 'w') as f:
        for proxy in working_proxies:
            f.write(proxy + '\n')
            
    print(f"\nFinished checking. Found {len(working_proxies)} working proxies.")
    print("List saved to working_proxies.txt")

if __name__ == "__main__":
    main()
