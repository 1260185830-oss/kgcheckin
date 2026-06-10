"""
三毛机场 → 小火箭 订阅转换
GitHub Actions 定时执行
"""
import requests
import yaml
import base64
import urllib.parse

AIRPORT_URL = "https://sub-1.smjcdh.top/smjc/api/v1/client/subscribe?token=b8c5293b3ebbe91ff72196f8f2e40dc8"
CLASH_UA = "clash-verge/v2.0.0"

def main():
    # 1. 用 Clash UA 拉机场真实配置
    resp = requests.get(AIRPORT_URL, headers={"User-Agent": CLASH_UA}, timeout=30)
    config = yaml.safe_load(resp.text)
    
    links = []
    for p in config.get("proxies", []):
        name = p.get("name", "unknown")
        ptype = p.get("type", "")
        server = p.get("server", "")
        port = p.get("port", 0)
        password = p.get("password", "") or p.get("uuid", "")
        sni = p.get("sni", "")
        encoded = urllib.parse.quote(name)
        
        try:
            if ptype == "anytls":
                link = f"vless://{password}@{server}:{port}?type=tcp&security=tls&sni={sni}&fp=chrome&allowInsecure=1#{encoded}"
            elif ptype == "trojan":
                link = f"trojan://{password}@{server}:{port}?peer={sni}&insecure=1#{encoded}"
            elif ptype == "hysteria2":
                srv = f"[{server}]" if ":" in server and not server.startswith("[") else server
                link = f"hysteria2://{password}@{srv}:{port}?sni={sni}&insecure=1#{encoded}"
            else:
                continue
            links.append(link)
        except Exception:
            continue
    
    content = "\n".join(links)
    b64 = base64.b64encode(content.encode()).decode()
    
    with open("sub/smjcdh_latest.txt", "w") as f:
        f.write(b64)
    
    print(f"✅ 转换完成: {len(links)} 个节点")
    for lt in ptype.split(","):
        pass

if __name__ == "__main__":
    main()
