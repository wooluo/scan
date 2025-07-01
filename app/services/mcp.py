# MCP自动化渗透服务层
import subprocess
import shutil
from typing import List, Dict
import os

TOOLS = {
    "subfinder": "https://github.com/projectdiscovery/subfinder/releases/latest/download/subfinder_linux_amd64.zip",
    "httpx": "https://github.com/projectdiscovery/httpx/releases/latest/download/httpx_linux_amd64.zip",
    "nuclei": "https://github.com/projectdiscovery/nuclei/releases/latest/download/nuclei_linux_amd64.zip",
    "naabu": "https://github.com/projectdiscovery/naabu/releases/latest/download/naabu_linux_amd64.zip"
}

TOOLS_BIN = {
    "subfinder": "./subfinder",
    "httpx": "./httpx",
    "nuclei": "./nuclei",
    "naabu": "./naabu"
}

COMMON_PORTS = {
    "top100": "1-1024,3306,3389,5432,6379,8080,8443,9000,9200,11211,27017,5000,7001,7002,8000,8888,27018,27019,50070,50030,50060,50010,50020,50090,60010,60020,60030,60040,60050,60060,60070,60080,60090,60100,60110,60120,60130,60140,60150,60160,60170,60180,60190,60200,60210,60220,60230,60240,60250,60260,60270,60280,60290,60300,60310,60320,60330,60340,60350,60360,60370,60380,60390,60400,60410,60420,60430,60440,60450,60460,60470,60480,60490,60500,60510,60520,60530,60540,60550,60560,60570,60580,60590,60600,60610,60620,60630,60640,60650,60660,60670,60680,60690,60700,60710,60720,60730,60740,60750,60760,60770,60780,60790,60800,60810,60820,60830,60840,60850,60860,60870,60880,60890,60900,60910,60920,60930,60940,60950,60960,60970,60980,60990,61000,61010,61020,61030,61040,61050,61060,61070,61080,61090,61100,61110,61120,61130,61140,61150,61160,61170,61180,61190,61200,61210,61220,61230,61240,61250,61260,61270,61280,61290,61300,61310,61320,61330,61340,61350,61360,61370,61380,61390,61400,61410,61420,61430,61440,61450,61460,61470,61480,61490,61500,61510,61520,61530,61540,61550,61560,61570,61580,61590,61600,61610,61620,61630,61640,61650,61660,61670,61680,61690,61700,61710,61720,61730,61740,61750,61760,61770,61780,61790,61800,61810,61820,61830,61840,61850,61860,61870,61880,61890,61900,61910,61920,61930,61940,61950,61960,61970,61980,61990,62000,62010,62020,62030,62040,62050,62060,62070,62080,62090,62100,62110,62120,62130,62140,62150,62160,62170,62180,62190,62200,62210,62220,62230,62240,62250,62260,62270,62280,62290,62300,62310,62320,62330,62340,62350,62360,62370,62380,62390,62400,62410,62420,62430,62440,62450,62460,62470,62480,62490,62500,62510,62520,62530,62540,62550,62560,62570,62580,62590,62600,62610,62620,62630,62640,62650,62660,62670,62680,62690,62700,62710,62720,62730,62740,62750,62760,62770,62780,62790,62800,62810,62820,62830,62840,62850,62860,62870,62880,62890,62900,62910,62920,62930,62940,62950,62960,62970,62980,62990,63000,63010,63020,63030,63040,63050,63060,63070,63080,63090,63100,63110,63120,63130,63140,63150,63160,63170,63180,63190,63200,63210,63220,63230,63240,63250,63260,63270,63280,63290,63300,63310,63320,63330,63340,63350,63360,63370,63380,63390,63400,63410,63420,63430,63440,63450,63460,63470,63480,63490,63500,63510,63520,63530,63540,63550,63560,63570,63580,63590,63600,63610,63620,63630,63640,63650,63660,63670,63680,63690,63700,63710,63720,63730,63740,63750,63760,63770,63780,63790,63800,63810,63820,63830,63840,63850,63860,63870,63880,63890,63900,63910,63920,63930,63940,63950,63960,63970,63980,63990,64000,64010,64020,64030,64040,64050,64060,64070,64080,64090,64100,64110,64120,64130,64140,64150,64160,64170,64180,64190,64200,64210,64220,64230,64240,64250,64260,64270,64280,64290,64300,64310,64320,64330,64340,64350,64360,64370,64380,64390,64400,64410,64420,64430,64440,64450,64460,64470,64480,64490,64500,64510,64520,64530,64540,64550,64560,64570,64580,64590,64600,64610,64620,64630,64640,64650,64660,64670,64680,64690,64700,64710,64720,64730,64740,64750,64760,64770,64780,64790,64800,64810,64820,64830,64840,64850,64860,64870,64880,64890,64900,64910,64920,64930,64940,64950,64960,64970,64980,64990,65000,65010,65020,65030,65040,65050,65060,65070,65080,65090,65100,65110,65120,65130,65140,65150,65160,65170,65180,65190,65200,65210,65220,65230,65240,65250,65260,65270,65280,65290,65300,65310,65320,65330,65340,65350,65360,65370,65380,65390,65400,65410,65420,65430,65440,65450,65460,65470,65480,65490,65500,65510,65520,65530,65535"
}

def check_tool_installed(tool: str) -> bool:
    return os.path.isfile(TOOLS_BIN[tool])

def download_tool(tool: str) -> bool:
    url = TOOLS[tool]
    zip_name = f"{tool}.zip"
    try:
        subprocess.run(["wget", "-O", zip_name, url], check=True)
        subprocess.run(["unzip", "-o", zip_name], check=True)
        os.chmod(TOOLS_BIN[tool], 0o755)
        os.remove(zip_name)
        return True
    except Exception as e:
        return False

def run_subfinder(domain: str) -> List[str]:
    if not check_tool_installed("subfinder"):
        raise RuntimeError("subfinder未安装")
    result = subprocess.run([TOOLS_BIN["subfinder"], "-d", domain, "-silent"], capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def run_httpx(input_list: List[str]) -> List[str]:
    if not check_tool_installed("httpx"):
        raise RuntimeError("httpx未安装")
    with open("b.txt", "w") as f:
        f.write("\n".join(input_list))
    result = subprocess.run([TOOLS_BIN["httpx"], "-list", "b.txt"], capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def run_nuclei(input_list: List[str]) -> List[str]:
    if not check_tool_installed("nuclei"):
        raise RuntimeError("nuclei未安装")
    with open("ur.txt", "w") as f:
        f.write("\n".join(input_list))
    result = subprocess.run([TOOLS_BIN["nuclei"], "-l", "ur.txt"], capture_output=True, text=True)
    return result.stdout.strip().splitlines()

def run_naabu(target: str, ports: str = None, rate: int = 1000, custom_ports: str = None) -> List[str]:
    if not check_tool_installed("naabu"):
        raise RuntimeError("naabu未安装")
    args = [TOOLS_BIN["naabu"], "-host", target, "-silent", "-rate", str(rate)]
    if ports:
        if ports in COMMON_PORTS:
            args += ["-p", COMMON_PORTS[ports]]
        else:
            args += ["-p", ports]
    elif custom_ports:
        args += ["-p", custom_ports]
    print(f"[DEBUG] naabu args: {args}")
    result = subprocess.run(args, capture_output=True, text=True)
    print(f"[DEBUG] naabu stdout: {result.stdout}")
    print(f"[DEBUG] naabu stderr: {result.stderr}")
    return result.stdout.strip().splitlines()

def auto_asset_and_vuln_scan(domain: str) -> Dict:
    subdomains = run_subfinder(domain)
    alive = run_httpx(subdomains)
    vulns = run_nuclei(alive)
    return {"subdomains": subdomains, "alive": alive, "vulns": vulns}

def auto_port_scan(target: str, ports: str = "top100", rate: int = 1000, custom_ports: str = None) -> Dict:
    open_ports = run_naabu(target, ports=ports, rate=rate, custom_ports=custom_ports)
    return {"target": target, "open_ports": open_ports}

def get_tool_status() -> Dict:
    return {tool: check_tool_installed(tool) for tool in TOOLS}

def download_missing_tools() -> Dict:
    status = {}
    for tool in TOOLS:
        if not check_tool_installed(tool):
            status[tool] = download_tool(tool)
        else:
            status[tool] = True
    return status

def run_asset_discovery(target: str) -> List[str]:
    """自动化资产发现，调用Yakit爬虫等"""
    # TODO: 调用Yakit CLI/API
    # 示例返回
    return ["/api/login", "/api/transfer"]

def analyze_endpoints(endpoints: List[str]) -> List[Dict]:
    """AI分析接口风险，调用Cherry Studio/知识库"""
    # TODO: Cherry Studio API + 本地知识库
    return [{"endpoint": ep, "risk": "high" if "admin" in ep else "medium"} for ep in endpoints]

def auto_vuln_scan(endpoint: str) -> List[Dict]:
    """自动化漏洞探测，集成Burp/Yakit"""
    # TODO: 调用Burp/Yakit扫描API
    return [{"type": "SQLi", "payload": "1' OR 1=1--", "confirmed": True}]

def ai_generate_poc(vuln_type: str, endpoint: str) -> str:
    """AI生成PoC，调用Cherry Studio"""
    # TODO: Cherry Studio生成PoC
    return f"# PoC for {vuln_type} on {endpoint}\nprint('Exploit!')"
