import requests
import time

BASE = "http://127.0.0.1:8000"

def login(username="admin", password="admin"):
    resp = requests.post(
        f"{BASE}/auth/login",
        data={
            "grant_type": "password",
            "username": username,
            "password": password
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    resp.raise_for_status()
    token = resp.json()["access_token"]
    return token

def portscan(token, target, ports="80,443", rate=1000, custom_ports=""):
    resp = requests.post(
        f"{BASE}/mcp/portscan",
        json={
            "target": target,
            "ports": ports,
            "rate": rate,
            "custom_ports": custom_ports
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"[DEBUG] /mcp/portscan 返回: {resp.text}")  # 调试输出
    return resp.json().get("open_ports", [])

def httpx_info(token, url):
    resp = requests.post(
        f"{BASE}/mcp/httpxinfo",
        json={"url": url},
        headers={"Authorization": f"Bearer {token}"}
    )
    return resp.json()

def vulnscan(token, url):
    resp = requests.post(
        f"{BASE}/mcp/vulnscan",
        json={"target": url},
        headers={"Authorization": f"Bearer {token}"}
    )
    return resp.json().get("vulnerabilities", [])

def test_specific_hosts(token, hosts):
    results = []
    for sub in hosts:
        ports = portscan(token, sub, ports="80,443")
        print(f"{sub} 开放端口: {ports}")
        for port in ports:
            # naabu返回的是 host:port，需要拆分
            if ':' in port:
                host, port_num = port.split(':', 1)
            else:
                host, port_num = sub, port
            url = f"http://{host}:{port_num}"
            try:
                info = httpx_info(token, url)
                print(f"{url} 站点信息: {info}")
            except Exception as e:
                info = {"error": str(e)}
                print(f"{url} httpx抓取失败: {e}")
            if info and info.get("status_code", 0) in [200, 301, 302]:
                vulns = vulnscan(token, url)
                print(f"{url} 漏洞: {vulns}")
            else:
                vulns = []
            results.append({"subdomain": sub, "port": port, "httpx_info": info, "vulnerabilities": vulns})
    print("完整扫描结果:")
    print(results)

def full_workflow(token, domain):
    # 只测试 www.example.com 和 f5.example.com
    subdomains = ["www.example.com", "f5.example.com"]
    print(f"测试子域名: {subdomains}")
    results = []
    for sub in subdomains:
        ports = portscan(token, sub, ports="80,443")
        print(f"{sub} 开放端口: {ports}")
        for port in ports:
            # naabu返回的是 host:port，需要拆分
            if ':' in port:
                host, port_num = port.split(':', 1)
            else:
                host, port_num = sub, port
            url = f"http://{host}:{port_num}"
            # httpx信息抓取
            try:
                info = httpx_info(token, url)
                print(f"{url} 站点信息: {info}")
            except Exception as e:
                info = {"error": str(e)}
                print(f"{url} httpx抓取失败: {e}")
            # 只对存活站点做漏洞扫描
            if info and info.get("status_code", 0) in [200, 301, 302]:
                vulns = vulnscan(token, url)
                print(f"{url} 漏洞: {vulns}")
            else:
                vulns = []
            results.append({"subdomain": sub, "port": port, "httpx_info": info, "vulnerabilities": vulns})
    print("完整扫描结果:")
    print(results)

if __name__ == "__main__":
    token = login()
    test_specific_hosts(token, ["www.example.com", "f5.example.com"])
