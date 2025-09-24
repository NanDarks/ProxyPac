import sys
import requests
import json
import os
import random

# A dictionary to map platform names to their rule sources
RULE_SOURCES = {
    'v2ray': 'https://raw.githubusercontent.com/Chocolate4U/Iran-v2ray-rules/main/iran.dat',
    'singbox': 'https://raw.githubusercontent.com/Chocolate4U/Iran-sing-box-rules/main/iran.sbox',
    'clash': 'https://raw.githubusercontent.com/Chocolate4U/Iran-clash-rules/main/ruleset/iran.yaml',
}

def get_proxy_list():
    """Fetches the list of working proxies from the file."""
    try:
        with open('working_proxies.txt', 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: 'working_proxies.txt' not found. Please run proxy_checker.py first.")
        return []

def get_rules(platform):
    """Fetches rules for a specific platform."""
    url = RULE_SOURCES.get(platform)
    if not url:
        return ""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Error fetching rules for {platform}: {response.status_code}")
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rules for {platform}: {e}")
        return ""

def generate_v2ray_config(proxy_list, rules):
    """Generates a V2ray config file."""
    if not proxy_list:
        return ""
    
    selected_proxy = random.choice(proxy_list)
    host, port = selected_proxy.split(':')
    
    config = {
        "outbounds": [
            {
                "protocol": "socks",
                "settings": {
                    "servers": [
                        {
                            "address": host,
                            "port": int(port),
                            "users": []
                        }
                    ]
                },
                "tag": "proxy"
            },
            {
                "protocol": "freedom",
                "tag": "direct"
            }
        ],
        "routing": {
            "domainStrategy": "AsIs",
            "rules": [
                {"type": "field", "outboundTag": "direct", "domain": ["geosite:ir"]},
                {"type": "field", "outboundTag": "proxy", "domain": ["geosite:google", "geosite:youtube", "geosite:twitter"]},
            ]
        }
    }
    
    # Simple obfuscation
    obfuscated_v2ray = json.dumps(config, indent=2)
    obfuscated_v2ray = obfuscated_v2ray.replace("proxy", "px").replace("direct", "drct")
    
    return obfuscated_v2ray

def generate_singbox_config(proxy_list, rules):
    """Generates a Sing-Box config file."""
    if not proxy_list:
        return ""
    
    selected_proxy = random.choice(proxy_list)
    host, port = selected_proxy.split(':')
    
    config = {
      "log": {
        "disabled": False,
        "level": "info",
        "timestamp": True
      },
      "outbounds": [
        {
          "type": "socks",
          "tag": "proxy",
          "server": host,
          "server_port": int(port)
        },
        {
          "type": "direct",
          "tag": "direct"
        },
        {
          "type": "block",
          "tag": "block"
        }
      ],
      "route": {
        "rule_set": [
          {
            "tag": "iran_rules",
            "format": "srs",
            "url": "https://raw.githubusercontent.com/Chocolate4U/Iran-sing-box-rules/main/iran.sbox"
          }
        ],
        "rules": [
          {
            "rule_set": "iran_rules",
            "outbound": "proxy"
          },
          {
            "domain_suffix": ["ir"],
            "outbound": "direct"
          },
          {
            "outbound": "proxy"
          }
        ]
      }
    }
    
    # Simple obfuscation
    obfuscated_singbox = json.dumps(config, indent=2)
    obfuscated_singbox = obfuscated_singbox.replace("proxy", "px").replace("direct", "drct")
    
    return obfuscated_singbox

def generate_clash_config(proxy_list, rules):
    """Generates a Clash config file."""
    if not proxy_list:
        return ""
    
    selected_proxy = random.choice(proxy_list)
    host, port = selected_proxy.split(':')
    
    config = {
        "proxies": [
            {
                "name": "Proxy",
                "type": "socks5",
                "server": host,
                "port": int(port)
            }
        ],
        "proxy-groups": [
            {
                "name": "Proxy-Group",
                "type": "select",
                "proxies": ["Proxy", "DIRECT"]
            }
        ],
        "rules": [
            "RULE-SET,iran,DIRECT",
            "GEOIP,IR,DIRECT",
            "MATCH,Proxy-Group"
        ]
    }
    
    # Add rules from the source
    if rules:
        config['rules'] = rules.split('\n') + config['rules']

    # Simple obfuscation
    obfuscated_clash = json.dumps(config, indent=2)
    obfuscated_clash = obfuscated_clash.replace("Proxy", "Px").replace("DIRECT", "DRCT")
    
    return obfuscated_clash

def main(platform):
    """Main function to generate config based on platform."""
    proxies = get_proxy_list()
    rules = get_rules(platform)
    
    config_content = ""
    if platform == "v2ray":
        config_content = generate_v2ray_config(proxies, rules)
    elif platform == "singbox":
        config_content = generate_singbox_config(proxies, rules)
    elif platform == "clash":
        config_content = generate_clash_config(proxies, rules)
    else:
        print(f"Error: Unsupported platform '{platform}'.")
        return

    if config_content:
        output_dir = platform
        os.makedirs(output_dir, exist_ok=True)
        
        if platform in ["v2ray", "singbox"]:
            filename = os.path.join(output_dir, "config.json")
        elif platform == "clash":
            filename = os.path.join(output_dir, "config.yaml")
        
        with open(filename, "w") as f:
            f.write(config_content)
        
        print(f"Successfully generated {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python config_generator.py <v2ray|singbox|clash>")
        sys.exit(1)
    
    platform_to_generate = sys.argv[1]
    main(platform_to_generate)
