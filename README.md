# self-sovereign-node
我的自我主權節點計畫:用設備進入Web3

我打算用 樹莓 Pi 打造一個屬於自己的「自我主權節點」，逐步實現以下目標：

- 第 1 階段：架設 VPN（WireGuard / Tailscale）：無論人在外面還是家裡，流量都能安全進出自己的節點（WireGuard / Tailscale）。
- 第 2 階段：建立私有雲（Nextcloud）：照片、文件同步到自己的伺服器（Nextcloud）
- 第 3 階段：導入去中心化元素（ENS、Web3 身份）：重要檔案可以上 IPFS 做備援與長期保存；未來結合 ENS / 智能合約，讓這個節點變成自己在 Web3 的「基地」。
- 第 4 階段：整合更多隱私工具與金融應用 ：逐步加入更多隱私工具、加密貨幣相關功能

此專案是我的學習紀錄與實作過程，未來也希望能成為他人參考。
定位是：**可實際使用的個人實驗場＋長期作品集**。

---

## 🔧 功能與進度

### ✅ 已完成 / 進行中

- [x] 樹莓派作為主節點設備安裝與基本設定  
- [x] 架設 WireGuard VPN（筆電 / 手機作為 client 連線）  
- [x] 設定節點為網路入口（VPN Gateway、流量轉送測試）  
- [x] 安裝並配置 Nextcloud 作為私有雲  
- [x] 安裝 IPFS 節點，測試 pin 檔案與基本操作  
- [ ] 將 Nextcloud 檔案與 IPFS 流程做部分整合（設計中）  
- [ ] 與 ENS / Web3 身份綁定（規劃中）  
- [ ] 自動化腳本（開機啟動、健康檢查、備份策略）  
- [ ] 更完整的安全威脅模型與防護配置文件  

---

## 🏗 系統概觀（v0.1）

目前的拓樸可以簡單描述為：

- **Raspberry Pi 3**：  
  - 跑 WireGuard server  
  - 跑 Nextcloud  
  - 跑 IPFS daemon  
- **Client 裝置**：  
  - 筆電（Windows）  
  - 手機  
  經由 WireGuard 連入 Pi，當作進入「自家內網」與私有雲的入口。

未來會補上系統架構圖與資料流圖（`/diagrams` 目錄）。

---

## 📁 專案結構（規劃中）

本 repo 預計整理成以下結構（隨進度調整）：

```text
self-sovereign-node/
├── README.md              # 專案說明（本檔案）
├── wireguard/             # VPN 相關設定與說明
│   ├── README.md
│   └── examples/
├── nextcloud/             # 私有雲部署與設定紀錄
│   └── README.md
├── ipfs/                  # IPFS 節點與腳本
│   └── README.md
├── device/                # 樹莓派系統層級設定
│   └── README.md
└── docs/                  # 進階說明與筆記
    ├── architecture.md
    ├── network-notes.md
    └── roadmap.md
