# Self-Node 控制台（Flask + Gunicorn + Nginx）

這個模組是跑在樹莓派上的一個「小型控制台」，  
用來在內網快速查看自我主權節點目前的狀態。

目前專案結構是將 Flask app 拆成三個主要模組：

- `app.py`：Flask 應用主入口，負責 routing 與頁面組合
- `auth.py`：處理 HTTP Basic Auth / session 檢查
- `collectors.py`：負責呼叫系統指令（如 `wg show`、`ipfs`、`last` 等），整理成卡片需要的資料格式


技術棧：

- Python 3
- Flask（Web framework）
- Gunicorn（WSGI server）
- Nginx 反向代理
- HTTP Basic Auth（簡單帳密保護）
- 僅開放內網存取（e.g. 192.168.x.x）

---

## 🎛 控制台功能卡片

首頁目前有四個資訊卡片：

### 1. VPN 狀態（WireGuard）

顯示內容包含：

- 目前是否連線中  
- 每個 peer 的：
  - public key
  - endpoint
  - allowed IPs
  - 最近握手時間（handshake）
  - 傳輸流量（received / sent）

資料來源：呼叫 `wg show`，再由後端解析結果後渲染到前端。

---

### 2. Nextcloud 使用量

顯示：

- 是否已安裝（Installed: true / false）
- Nextcloud 版本（Version）
- 使用中的儲存空間（Data usage）

資料來源：  
透過系統指令或 Nextcloud 提供的 CLI / API 抓取目前安裝狀態與使用量，  
由 Flask 後端轉成數字後顯示在卡片上。

---

### 3. IPFS 狀態

顯示：

- IPFS Online 狀態（true/false）
- Peer ID
- Peers 數量
- Repo size（本地儲存使用量）

資料來源：  
呼叫 `ipfs id`、`ipfs stats repo` 等指令取得資訊，  
並在頁面上以簡潔文字呈現。

---

### 4. 最近登入紀錄

顯示：

- 最近登入系統的使用者、來源 IP、時間  
- 像是 `last` 指令輸出的整理版  

用途：

- 快速確認是否有異常登入  
- 當作簡單的安全監控面板

---

## 🔐 安全設計

- 控制台只聽在內部位址（例如：`127.0.0.1:8081` 或內網 IP）  
- 由 Nginx 做反向代理後再轉出  
- 使用 HTTP Basic Auth 做基本帳密保護  
- 不開放公網，只允許內網存取（例如：`192.168.0.x:8081`）

這樣的設計適合：

- 家用 / 自託管環境  
- 不需要對全世界開一個管理後台  
- 但又希望在同一個網段內，可以從筆電或手機快速查看節點狀態

---

## 📁 預計檔案結構（之後可慢慢補）

```text
dashboard/
dashboard/
├── README.md                 # 本檔案
├── app.py                    # Flask 入口，啟動控制台
├── auth.py                   # HTTP Basic Auth / 權限相關邏輯
├── collectors.py             # 取得 VPN / IPFS / Nextcloud / 登入紀錄的後端程式
├── static/                   # 前端靜態資源（CSS / 圖片等）
│   └── app.css                  
└── templates/                # HTML 模板（index.html）
    └── index.html
  
