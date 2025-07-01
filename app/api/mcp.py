from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.core.jwt import get_current_user
from app.services.save_result import save_scan_result
from app.services.save_tables import save_asset, save_port_scan, save_vuln_scan
import subprocess
import uuid
import threading
import time

router = APIRouter()

# 全局任务进度存储（生产环境建议用Redis等持久化存储）
workflow_progress = {}

def run_subfinder(domain):
    result = subprocess.run([
        "./subfinder", "-d", domain, "-silent"
    ], capture_output=True, text=True, timeout=30)
    return result.stdout.strip().splitlines()

def run_naabu(target, ports="top100", rate=1000, custom_ports=None):
    if custom_ports:
        cmd = ["./naabu", "-host", target, "-p", custom_ports, "-rate", str(rate), "-silent"]
    else:
        cmd = ["./naabu", "-host", target, "-top-ports", str(ports), "-rate", str(rate), "-silent"]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return result.stdout.strip().splitlines()

def run_httpx(url):
    result = subprocess.run(
        ["./httpx", "-u", url, "-title", "-status-code", "-silent"],
        capture_output=True, text=True, timeout=20
    )
    return result.stdout.strip()

def run_nuclei(url):
    result = subprocess.run(
        ["./nuclei", "-u", url, "-silent"],
        capture_output=True, text=True, timeout=60
    )
    return result.stdout.strip().splitlines()

def workflow_task(domain, task_id):
    try:
        workflow_progress[task_id] = {"percent": 5, "step": "子域名发现中"}
        subdomains = run_subfinder(domain)
        result = []
        total = len(subdomains)
        done = 0
        for sub in subdomains:
            workflow_progress[task_id] = {"percent": int(5 + 80 * done / max(total,1)), "step": f"{sub} 端口扫描中"}
            open_ports = run_naabu(sub)
            for port in open_ports:
                url = f"http://{sub}:{port}"
                workflow_progress[task_id] = {"percent": int(5 + 80 * done / max(total,1)), "step": f"{url} httpx探测中"}
                httpx_info = run_httpx(url)
                # 解析httpx_info
                if httpx_info:
                    # 解析title、status_code、ip
                    title, status_code, ip = None, None, None
                    try:
                        parts = httpx_info.split()
                        for p in parts:
                            if p.startswith("[title:"):
                                title = p[7:-1]
                            elif p.startswith("[status-code:"):
                                status_code = int(p[13:-1])
                            elif p.startswith("[ip:"):
                                ip = p[4:-1]
                    except:
                        pass
                    workflow_progress[task_id] = {"percent": int(5 + 80 * done / max(total,1)), "step": f"{url} 漏洞扫描中"}
                    vulns = run_nuclei(url)
                    vuln_info = ",".join(vulns) if vulns else None
                    # 保存到数据库
                    save_scan_result(domain, ip or sub, int(port), title, status_code, vuln_info)
                else:
                    vulns = []
                result.append({
                    "subdomain": sub,
                    "port": port,
                    "httpx_info": httpx_info,
                    "vulnerabilities": vulns
                })
            done += 1
        workflow_progress[task_id] = {"percent": 100, "step": "完成", "result": result}
    except Exception as e:
        workflow_progress[task_id] = {"percent": -1, "step": f"失败: {e}"}

@router.post("/workflow")
def full_scan_workflow(request: dict, background_tasks: BackgroundTasks, user=Depends(get_current_user)):
    domain = request.get("domain")
    if not domain:
        raise HTTPException(status_code=400, detail="缺少domain参数")
    task_id = str(uuid.uuid4())
    workflow_progress[task_id] = {"percent": 0, "step": "排队中"}
    background_tasks.add_task(workflow_task, domain, task_id)
    return {"task_id": task_id}

@router.get("/workflow/progress")
def get_workflow_progress(task_id: str, user=Depends(get_current_user)):
    prog = workflow_progress.get(task_id)
    if not prog:
        raise HTTPException(status_code=404, detail="任务不存在")
    return prog

@router.post("/quickscan")
def quick_asset_and_vuln_scan(request: dict, user=Depends(get_current_user)):
    domain = request.get("domain")
    if not domain:
        raise HTTPException(status_code=400, detail="缺少domain参数")
    try:
        subfinder_result = subprocess.run(
            ["./subfinder", "-d", domain, "-silent"],
            capture_output=True, text=True, timeout=30
        )
        subdomains = subfinder_result.stdout.strip().splitlines()
        # 保存资产发现结果
        for sub in subdomains:
            save_asset(domain, sub)
        return {"subdomains": subdomains}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"subfinder执行失败: {e}")

@router.post("/portscan")
def port_scan(request: dict, user=Depends(get_current_user)):
    target = request.get("target")
    ports = request.get("ports", "top100")
    rate = request.get("rate", 1000)
    custom_ports = request.get("custom_ports")
    if not target:
        raise HTTPException(status_code=400, detail="缺少target参数")
    try:
        # 判断参数类型，决定naabu命令
        if custom_ports:
            cmd = ["./naabu", "-host", target, "-p", custom_ports, "-rate", str(rate), "-silent"]
        elif str(ports).startswith("top") and str(ports)[3:].isdigit():
            # 例如top100、top1000
            cmd = ["./naabu", "-host", target, "-top-ports", str(ports)[3:], "-rate", str(rate), "-silent"]
        else:
            # 例如80,443等自定义端口
            cmd = ["./naabu", "-host", target, "-p", str(ports), "-rate", str(rate), "-silent"]
        naabu_result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        open_ports = naabu_result.stdout.strip().splitlines()
        # 保存端口扫描结果
        for port in open_ports:
            save_port_scan(target, target, int(port), status="open")
        return {"open_ports": open_ports}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"naabu执行失败: {e}")

@router.post("/vulnscan")
def vuln_scan(request: dict, user=Depends(get_current_user)):
    target = request.get("target")
    if not target:
        raise HTTPException(status_code=400, detail="缺少target参数")
    try:
        nuclei_result = subprocess.run(
            ["./nuclei", "-u", target, "-silent"],
            capture_output=True, text=True, timeout=60
        )
        vulns = nuclei_result.stdout.strip().splitlines()
        # 保存漏洞扫描结果
        for vuln in vulns:
            save_vuln_scan(target, target, 80, vuln)  # 这里只能简单保存，建议解析target和端口
        return {"vulnerabilities": vulns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"nuclei执行失败: {e}")

@router.post("/httpxinfo")
def httpx_info(request: dict, user=Depends(get_current_user)):
    url = request.get("url")
    if not url:
        raise HTTPException(status_code=400, detail="缺少url参数")
    try:
        result = subprocess.run(
            ["./httpx", "-u", url, "-title", "-status-code", "-content-length", "-server", "-ip", "-silent", "-json"],
            capture_output=True, text=True, timeout=20
        )
        # httpx -json 每行一个json对象
        lines = result.stdout.strip().splitlines()
        if not lines:
            return {"error": "httpx无输出"}
        import json
        info = json.loads(lines[0])
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"httpx执行失败: {e}")

@router.get("/tools/status")
def tools_status(user=Depends(get_current_user)):
    import shutil
    status = {
        "subfinder": shutil.which("subfinder") is not None,
        "naabu": shutil.which("naabu") is not None,
        "nuclei": shutil.which("nuclei") is not None,
    }
    return status
