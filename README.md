# self-sovereign-node
我的自我主權節點計畫:用設備進入Web3

我用 樹莓 Pi 打造一個屬於自己的「自我主權節點」，實現以下目標：

- 第 1 階段：架設 VPN（WireGuard）：無論人在外面還是家裡，流量都能安全進出自己的節點（WireGuard）。
- 第 2 階段：建立私有雲（Nextcloud）：照片、文件同步到自己的伺服器（Nextcloud）
- 第 3 階段：導入去中心化元素（ENS、Web3 身份）：重要檔案可以上 IPFS 做備援與長期保存；
      未來結合 ENS / 智能合約，讓這個節點變成自己在 Web3 的「基地」。
- 第 4 階段：在 Pi 上跑一個 Flask Dashboard，即時顯示 VPN / Nextcloud / IPFS / 登入紀錄。
- 第 5 階段：加上 UFW / Fail2ban / SSH 2FA 等防護。

此專案是我的學習紀錄與實作過程，未來也希望能成為他人參考。
定位是：**可實際使用的個人實驗場＋長期作品集**。

## 🔧 功能與進度

### ✅ 已完成 / 進行中

- [x] 樹莓派作為主節點設備安裝與基本設定  
- [x] 架設 WireGuard VPN（筆電 / 手機作為 client 連線）  
- [x] 設定節點為網路入口（VPN Gateway、流量轉送測試）  
- [x] 安裝並配置 Nextcloud 作為私有雲  
- [x] 安裝 IPFS 節點，測試 pin 檔案與基本操作  
- [x] 將 Nextcloud 檔案與 IPFS 流程做部分整合  
- [x] 定期把節點快照（hash）上鏈 Arbitrum Sepolia 
- [x] Flask Dashboard 顯示 VPN / Nextcloud / IPFS / 登入紀錄
- [x] 加上 UFW / Fail2ban / SSH 2FA 等防護 


## 🏗 系統概觀


- **Raspberry Pi 3**：  
  - 跑 WireGuard server  
  - 跑 Nextcloud  
  - 跑 IPFS daemon  
- **Client 裝置**：  
  - 筆電（Windows）  
  - 手機  
  經由 WireGuard 連入 Pi，當作進入「自家內網」與私有雲的入口，讓設備能互相溝通。



## 📁 專案結構

本 repo 整理成以下結構：

self-sovereign-node/
├── README.md                      # 專案總說明（整體故事 / 架構 / 模組總覽）

├── wireguard/                     # VPN 相關設定與說明
│   ├── README.md                  # WireGuard 整體說明、Pi 當 server 的架構
│   ├── server-example.conf        # 伺服器端設定範例（已去除私鑰）
│   ├── client-example.conf        # Client 端設定範例（筆電 / 手機）
│   └── gateway-notes.md           # Pi 當 VPN gateway 的路由 / 轉發 / 防火牆備忘

├── nextcloud/                     # 私有雲部署與設定紀錄
│   ├── README.md                  # Nextcloud 在 Pi 上的安裝與整體說明
│   ├── config-example.php         # config.php 範例（敏感資訊改為 placeholder）
│   ├── install-notes.md           # 安裝過程、指令、踩過的坑紀錄
│   ├── issues.md                  # 遇到的問題與解法（debug log）
│   └── public-folder-notes.md     # 用於「公開資料夾 → IPFS」的結構與使用方式

├── ipfs/                          # IPFS 節點與同步腳本
│   ├── README.md                  # IPFS 節點角色與在此專案中的定位
│   ├── commands-notes.md          # 常用 ipfs 指令與範例（repo stat / swarm / pin 等）
│   └── nextcloud_ipfs_sync.sh     # 將 Nextcloud 公開資料夾同步到 IPFS 並 PIN 的腳本

├── ens/                           # ENS 綁定 IPFS / 節點資料的流程紀錄
│   ├── README.md                  # ENS 在專案中的用途說明
│   └── dk45dola-setup.md          # 以 dk45dola.eth 為例的實際設定步驟與紀錄

├── onchain-sync/                  # 節點狀態快照上鏈（Arbitrum Sepolia）
│   ├── README.md
│   ├── vpn_anchor.py              # 從 WireGuard 快照計算 SHA256 並送出交易
│   ├── .env.example               # RPC / 私鑰 / WG_IFACE 等環境變數樣板
│   └── systemd/
│       ├── vpn-anchor.service.example
│       └── vpn-anchor.timer.example

├── dashboard/                     # Pi 上的 Flask 控制台
│   ├── README.md
│   ├── app.py                     # Flask 入口：/ 與 /api/status
│   ├── auth.py                    # HTTP Basic Auth（從 .env 讀帳密）
│   ├── collectors.py              # 收集 VPN / Nextcloud / IPFS / 登入紀錄
│   ├── templates/
│   │   └── index.html             # 4 張卡片的前端頁面
│   └── static/
│       └── app.css                # 卡片 / peer list / login list 樣式

├── device/                        # 樹莓派系統層級設定（OS / 硬體 / SSH 等）
│   └── README.md
│ 
│ 還沒想

## 技術關鍵字包含：

- Linux / Raspberry Pi
- WireGuard / VPN
- Nextcloud / LAMP stack
- IPFS / CID / content addressing
- ENS / eth.limo
- Arbitrum Sepolia / Web3.py / systemd timer
- Flask dashboard / Basic Auth
- UFW / Fail2ban / SSH 2FA
