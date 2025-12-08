# IPFS 節點設定與 Nextcloud 同步

本資料夾用來紀錄 self-sovereign-node 中的 IPFS 配置、指令、與與 Nextcloud 的自動化整合流程。

IPFS 在本專案中的角色：

- 作為「不可變、去中心化」檔案備份層  
- 保存 Nextcloud 特定資料夾中的檔案  
- 讓重要內容在本地硬碟之外也有備份  
- 未來可與 ENS 做更高階的檔案定位（CID 綁定）  

---

## 🔧 IPFS 基本功能（目前進度）

- 安裝與初始化完成  
- 可正常啟動 IPFS daemon  
- 支援 `ipfs add`、`ipfs pin add` 等操作  
- 已完成 Nextcloud → IPFS 自動同步流程（重點）  

---

## 🔁 Nextcloud → IPFS 自動備份流程（已建立）

本專案的其中一個功能，是讓 Nextcloud 的「公開資料夾」能夠自動被同步到 IPFS。

### 📁 1. Nextcloud 公開資料夾位於：

（實際路徑之後會補上）

### 📜 2. 自動同步腳本位置：
（實際路徑之後會補上）


### ⚙️ 3. 腳本功能摘要：

- 檢查 Nextcloud 公開資料夾是否有變化  
- 將變化的檔案計算 CID  
- 執行 `ipfs add` 新增檔案  
- 自動 `ipfs pin add` 固定檔案  
- 回傳 CID（可日後加入 ENS 或 API）

### 🧠 4. 為什麼要這樣做？

因為：

- Nextcloud＝可編輯、可更新的檔案  
- IPFS＝不可變、永久的內容雜湊  

兩者結合可以獲得：

- 檔案可版本化  
- 長期保存  
- 不受伺服器損壞影響  
- 未來可將 CID 公開（或綁 ENS）  

---

## 📌 未來規劃（待加入）

- 將腳本加入 systemd，確保自動執行  
- 建立 CID 索引（JSON database）  
- 增加 webhook，將 CID 傳回 Nextcloud UI  
- 與 ENS 做 CID 公告（IPNS 或 subdomain）  

---

## 📚 相關指令（之後會補）

ipfs daemon
ipfs add <file>
ipfs pin add <CID>
ipfs ls
ipfs cat <CID>
