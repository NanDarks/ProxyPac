import random

def generate_pac_file():
    try:
        with open("working_proxies.txt", "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: working_proxies.txt not found.")
        return

    if not proxies:
        print("No working proxies found. PAC file will not be generated.")
        return

    # Use a random proxy to distribute load and improve performance
    http_proxy = f"PROXY {random.choice(proxies)}"
    socks_proxy = f"SOCKS5 {random.choice(proxies)}"

    # List of filtered domains to be proxied
    filtered_domains = [
        "*.youtube.com",
        "*.googlevideo.com",
        "*.twitter.com",
        "*.instagram.com",
        "*.telegram.org",
        "*.wikipedia.org",
        "*.facebook.com",
        "*.linkedin.com",
        "*.tiktok.com"
    ]

    pac_content = """function FindProxyForURL(url, host) {
  // Use a random proxy from the list
  var proxies = ["%s"];
  var proxy = proxies[Math.floor(Math.random() * proxies.length)];

  // Domains that should be proxied
  var domains = [
    %s
  ];
  
  // If the host matches one of the domains, use the proxy
  for (var i = 0; i < domains.length; i++) {
    if (shExpMatch(host, domains[i])) {
      return proxy;
    }
  }

  // All other traffic goes directly
  return "DIRECT";
}
""" % (f"{http_proxy}; {socks_proxy}", ",\n    ".join([f'"{d}"' for d in filtered_domains]))

    with open("proxy.pac", "w") as f:
        f.write(pac_content)
    
    print("proxy.pac file generated successfully.")

if __name__ == "__main__":
    generate_pac_file()
