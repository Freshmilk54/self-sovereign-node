# On-chain Sync System (Arbitrum Sepolia)

本資料夾紀錄 self-sovereign-node 中「定時上鏈快照」的完整流程。

此功能的目標是將節點的關鍵狀態（VPN、Nextcloud、IPFS、meta snapshot）生成加密摘要（SHA256），並作為交易 data 上鏈保存，用作：

- 節點狀態證明  
- 日誌防篡改  
- 去中心化審計紀錄  
- 自我主權系統的 timestamp proof  

---

## 🔍 快照資料來源（目前整合）

### 1. WireGuard 設定快照  
來自：
wg show

解析後寫入 CSV（包含 peer 狀態、傳輸 bytes、最新 handshake 等）

### 2. 本地系統紀錄 CSV  
此 CSV 會包含節點運行狀態與基本健康指標。

### 3. IPFS / Nextcloud metadata（規劃中）

---

## 🔐 摘要（Snapshot Hash）計算方式

使用 SHA256：
sha256(snapshot.csv) → 得到 32 bytes hash

此 hash 會作為交易的 `data` 欄位上鏈。

---

## 🚀 上鏈流程：Arbitrum Sepolia（已完成）

1. 準備私鑰（測試網）  
2. RPC 設定 Arbitrum Sepolia  
3. 使用 web3.py / ethers.js 發送交易  
4. 將 snapshot hash 放入 transaction data  
5. 交易成功後，紀錄 tx hash 作為外部證據鏈

---

## 🕒 自動化流程

目前已設定定時任務：

- 呼叫 snapshot 腳本  
- 計算 SHA256  
- 發送交易上鏈  
- 記錄本地 log  

未來會改成：

- systemd timer  
- 可選擇不同鏈（Base、Arbitrum、Linea）

---

## 📌 例子（以 pseudo code 表示）

```python
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://sepolia-rollup.arbitrum.io/rpc"))

snapshot_hash = calc_sha256("snapshot.csv")

tx = {
    "to": "0x0000000000000000000000000000000000000000",
    "data": snapshot_hash,
    "gas": 50000,
    "nonce": w3.eth.get_transaction_count(account),
}

signed = w3.eth.account.sign_transaction(tx, private_key)
w3.eth.send_raw_transaction(signed.rawTransaction)


