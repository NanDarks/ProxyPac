import requests
from concurrent.futures import ThreadPoolExecutor

# Define proxy sources
proxy_sources = [
    "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt",
    "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all",
    "https://www.sslproxies.org/"
]

# Function to check if a proxy is working
def check_proxy(proxy):
    try:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}'
        }
        test_url = "https://www.google.com"
        requests.get(test_url, proxies=proxies, timeout=10)
        print(f"✅ {proxy} is working!")
        return proxy
    except Exception as e:
        return None

# Main function to get and check proxies
def get_working_proxies():
    all_proxies = set()
    for url in proxy_sources:
        try:
            response = requests.get(url, timeout=10)
            proxies = response.text.splitlines()
            all_proxies.update(proxies)
            print(f"Found {len(proxies)} proxies from {url}")
        except:
            print(f"Could not fetch from {url}")

    working_proxies = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(check_proxy, all_proxies)
        for result in results:
            if result:
                working_proxies.append(result)

    return working_proxies

# Run the program and save output to file
if __name__ == "__main__":
    healthy_proxies = get_working_proxies()
    with open("working_proxies.txt", "w") as f:
        for p in healthy_proxies:
            f.write(p + "\n")
    print("\n--- Summary ---")
    print(f"Total working proxies found: {len(healthy_proxies)}")
    print("List of working proxies saved to working_proxies.txt")
