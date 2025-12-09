import subprocess
import re
import time

# ------------------------------------------------------------
# 小工具：執行指令
# ------------------------------------------------------------

def _run(cmd: str, timeout: int = 5):
    """
    執行一條 shell 指令，回傳 (ok, output_or_error)。
    用 sudo -n，不會卡在密碼提示。
    """
    try:
        p = subprocess.run(
            cmd,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        if p.returncode == 0:
            return True, p.stdout.strip()
        return False, (p.stderr or p.stdout).strip()
    except Exception as e:
        return False, str(e)


# ------------------------------------------------------------
# VPN 狀態（WireGuard）
# ------------------------------------------------------------

def vpn_status():
    ok, out = _run("sudo -n wg show")
    if not ok:
        return {
            "up": False,
            "peers": [],
            "raw_ok": False,
            "error": out,
        }

    peers = []
    cur = {}

    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue

        # interface: wg0  ...  這行略過
        if line.startswith("interface:"):
            continue

        if line.startswith("peer:"):
            # 換新 peer 前，把上一個收進去
            if cur:
                peers.append(cur)
            cur = {"peer": line.split("peer:", 1)[1].strip()}

        elif "endpoint:" in line:
            cur["endpoint"] = line.split("endpoint:", 1)[1].strip()

        elif "allowed ips:" in line:
            raw = line.split("allowed ips:", 1)[1].strip()
            cur["allowed_ips"] = [ip.strip() for ip in raw.split(",")]

        elif "latest handshake:" in line:
            cur["handshake"] = line.split("latest handshake:", 1)[1].strip()

        elif "transfer:" in line:
            cur["transfer"] = line.split("transfer:", 1)[1].strip()

    if cur:
        peers.append(cur)

    return {
        "up": True,
        "peers": peers,
        "raw_ok": True,
    }


# ------------------------------------------------------------
# Nextcloud 使用量
# ------------------------------------------------------------

def _human_bytes(n):
    """把位元組數變成可讀格式"""
    try:
        n = int(n)
    except Exception:
        # 如果根本不是數字，就原樣回傳
        return str(n)

    units = ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
    i = 0
    f = float(n)
    while f >= 1024 and i < len(units) - 1:
        f /= 1024.0
        i += 1
    return f"{f:.1f} {units[i]}"


def nextcloud_usage():
    # 依你實際環境調整 occ 路徑 & data 目錄
    occ_cmd = "sudo -n -u www-data php /var/www/nextcloud/occ status"
    du_cmd  = "sudo du -sb /srv/nextcloud-data | awk '{print $1}'"

    ok1, status_out = _run(occ_cmd)
    ok2, du_out = _run(du_cmd)

    installed = False
    version = "unknown"

    if ok1:
        installed = ("installed: true" in status_out.lower())
        m = re.search(r"version:\s*([^\n\r]+)", status_out, re.I)
        if m:
            version = m.group(1).strip()

    data_usage = _human_bytes(du_out) if ok2 else "n/a"

    return {
        "installed": installed,
        "version": version,
        "data_usage": data_usage,
        "raw_ok": ok1 and ok2,
    }


# ------------------------------------------------------------
# IPFS 狀態
# ------------------------------------------------------------

def ipfs_status():
    ok1, id_out = _run("ipfs id -f='<id>'")
    ok2, peers_out = _run("ipfs swarm peers | wc -l")

    # 優先用 human 版 repo stat
    ok3h, repo_h = _run("ipfs repo stat --human")
    repo_size = "n/a"

    if ok3h:
        for line in repo_h.splitlines():
            if line.lower().startswith("reposize"):
                repo_size = line.split(":", 1)[1].strip()
                break
    else:
        ok3b, repo_b = _run("ipfs repo stat")
        if ok3b:
            for line in repo_b.splitlines():
                if line.lower().startswith("reposize"):
                    raw = line.split(":", 1)[1].strip()
                    repo_size = _human_bytes(raw)
                    break

    try:
        peers = int(peers_out) if ok2 else 0
    except Exception:
        peers = 0

    return {
        "online": ok1,
        "peer_id": id_out if ok1 else "",
        "peers": peers,
        "repo_size": repo_size,
        "raw_ok": ok1 and ok2 and (ok3h or repo_size != "n/a"),
    }


# ------------------------------------------------------------
# 最近登入紀錄
# ------------------------------------------------------------

def login_records():
    cmd = "last -n 8 -F | grep -vE '(reboot|shutdown)' | head -n 8"
    ok, out = _run(cmd)
    lines = out.splitlines() if ok else [out]
    return {
        "entries": lines,
        "raw_ok": ok,
    }


# ------------------------------------------------------------
# snapshot：給 /api/status 用
# ------------------------------------------------------------

_last_ts = 0
_last_snap = None


def snapshot():
    global _last_ts, _last_snap
    now = time.time()

    # 5 秒內多次呼叫就直接回 cache，避免每次都砍外部指令
    if _last_snap is not None and now - _last_ts < 5:
        return _last_snap

    _last_snap = {
        "vpn":       vpn_status(),
        "nextcloud": nextcloud_usage(),
        "ipfs":      ipfs_status(),
        "logins":    login_records(),
    }
    _last_ts = now
    return _last_snap
