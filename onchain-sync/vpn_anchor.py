
import os, subprocess, json, time, hashlib, datetime
from pathlib import Path

LOG_DIR = Path("<你的路徑>")
ENV_FILE = "<環境路徑>"

def run(cmd:list) -> str:
    return subprocess.check_output(cmd, text=True).strip()

def load_env(path):
    env = {}
    if Path(path).exists():
        for line in Path(path).read_text().splitlines():
            line=line.strip()
            if not line or line.startswith("#"): continue
            k,v = line.split("=",1)
            env[k.strip()] = v.strip()
    return env

def wg_dump(iface):
    out = run(["wg", "show", iface, "dump"]).splitlines()
    peers=[]
    for i, line in enumerate(out):
        if i==0:  # 第一行是介面資訊，跳過
            continue
        cols = line.split('\t')
        peer = {
            "pubkey": cols[0],
            "endpoint": cols[2],
            "allowed_ips": cols[3],
            "latest_handshake": int(cols[4]),
            "rx_bytes": int(cols[5]),
            "tx_bytes": int(cols[6]),
            "persistent_keepalive": cols[7],
        }
        peers.append(peer)
    return peers

def snapshot(iface):
    ts = int(time.time())
    return {
        "timestamp": ts,
        "iso": datetime.datetime.utcfromtimestamp(ts).isoformat()+"Z",
        "iface": iface,
        "peers": wg_dump(iface),
    }

def write_logs(data):
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # 追加 CSV
    csv = LOG_DIR/"traffic.csv"
    if not csv.exists():
        csv.write_text("iso,pubkey,allowed_ips,rx_bytes,tx_bytes,endpoint\n")
    with csv.open("a") as f:
        for p in data["peers"]:
            f.write(f'{data["iso"]},{p["pubkey"]},{p["allowed_ips"]},{p["rx_bytes"]},{p["tx_bytes"]},{p["endpoint"]}\n')

    # 每筆快照也丟到當日 JSON
    day = data["iso"][:10].replace("-","")
    with (LOG_DIR/f"traffic-{day}.json").open("a") as f:
        f.write(json.dumps(data, separators=(",",":"), ensure_ascii=False) + "\n")

    # 算 SHA256（針對這次快照本身）
    digest = hashlib.sha256(json.dumps(data, separators=(",",":"), sort_keys=True).encode()).hexdigest()
    (LOG_DIR/"last_hash.txt").write_text(digest+"\n")
    return digest

def anchor_onchain(digest, env):
    if env.get("ANCHOR_ENABLE","0") != "1":
        return None
    from web3 import Web3
    rpc = env["WEB3_RPC"]; chain_id = int(env["CHAIN_ID"])
    pk  = env["WALLET_PRIVATE_KEY"]; to = env["ANCHOR_TO"]
    w3 = Web3(Web3.HTTPProvider(rpc))
    acct = w3.eth.account.from_key(pk)
    nonce = w3.eth.get_transaction_count(acct.address)
    gas_price = w3.eth.gas_price  # Arbitrum 

    tx = {
        "to": Web3.to_checksum_address(to),
        "value": 0,
        "data": bytes.fromhex(digest),
        "nonce": nonce,
        "gas": 80000,
        "gasPrice": gas_price,
        "gasPrice": gas_price,
        "chainId": chain_id,
    }
    signed = w3.eth.account.sign_transaction(tx, pk)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction).hex()
    (LOG_DIR/"last_tx.txt").write_text(tx_hash+"\n")
    return tx_hash


def main():
    env = load_env(ENV_FILE)
    iface = env.get("WG_IFACE","wg0")
    data = snapshot(iface)
    digest = write_logs(data)
    txh = anchor_onchain(digest, env)

    print(f'snapshot peers={len(data["peers"])}')
    print("sha256:", digest)
    if txh: print("tx:", txh)

if __name__ == "__main__":
    main()
