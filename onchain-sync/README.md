# On-chain Sync System（VPN Snapshot Anchor）

這個模組負責把節點的 WireGuard 流量狀態快照：

1. 從 `wg show <iface> dump` 抓出所有 peer 的統計
2. 寫入本機 log（CSV + JSON）
3. 對這次快照內容計算 `SHA256`
4. 將 hash 當作交易 data，送到 Arbitrum Sepolia（測試網）
5. 透過 systemd timer 定期執行

目標是：為自我主權節點建立一條「可驗證的歷史軌跡」，  
讓每次狀態快照都在鏈上留下一個不可竄改的指紋。

---

## 🔁 資料流

簡化流程：

1. `vpn_anchor.py`：
   - 呼叫 `wg show wg0 dump`
   - 整理成結構化資料：
     - pubkey / endpoint / allowed_ips / rx_bytes / tx_bytes / latest_handshake
   - 寫入：
     - `/var/log/vpn/traffic.csv`（累積型 log）
     - `/var/log/vpn/traffic-YYYYMMDD.json`（每日 JSON 行檔）
   - 將本次快照 JSON 做 `SHA256`，寫入：
     - `/var/log/vpn/last_hash.txt`

2. 如果 `.env` 中 `ANCHOR_ENABLE=1`：
   - 從 `.env` 載入 RPC / 私鑰 / 鏈 ID / 目標地址
   - 組一筆 0 ETH 交易，`data` 欄位放入該 SHA256（32 bytes）
   - 使用 `web3.py` 簽署並發送到 Arbitrum Sepolia
   - 將 tx hash 寫入 `/var/log/vpn/last_tx.txt`

3. systemd：
   - `vpn-anchor.service`：負責「跑一次快照＋上鏈」
   - `vpn-anchor.timer`：每 5 分鐘叫 service 跑一次

---

## 📁 檔案一覽

- `vpn_anchor.py`  
  主程式，邏輯包含：
  - 讀取 WireGuard 介面狀態
  - 寫入 CSV / JSON log
  - 計算 SHA256、寫入 `last_hash.txt`
  - 在啟用時將 hash 上鏈並寫入 `last_tx.txt`

- `.env.example`  
  範例設定檔，實際部署時應建立 `/opt/vpn-anchor/.env`，內容包括：
  - `ANCHOR_ENABLE`
  - `WEB3_RPC`
  - `CHAIN_ID`
  - `WALLET_PRIVATE_KEY`
  - `ANCHOR_TO`
  - `WG_IFACE`

- `systemd/vpn-anchor.service.example`  
  供複製到 `/etc/systemd/system/vpn-anchor.service` 使用的 service 範例。

- `systemd/vpn-anchor.timer.example`  
  供複製到 `/etc/systemd/system/vpn-anchor.timer` 使用的 timer 範例。
