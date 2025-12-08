# ENS 設定與 CID 綁定流程

本資料夾紀錄我在 self-sovereign-node 中使用 ENS 的方式，以及將 IPFS CID 綁定到 ENS，使其可以透過 eth.limo / eth.link gateway 對外展示。

---

## 🌐 ENS Domain Used

目前使用的 ENS 名稱：
dk45dola.eth

對外瀏覽頁面（eth.limo）：
https://dk45dola.eth.limo/


此 gateway 會自動解析 ENS 記錄中的 `contenthash`，並展示對應的 IPFS CID 內容。

---

## 📦 功能摘要

- 租用 ENS 網域  
- 將 IPFS CID 綁定到 ENS（設定 contenthash）  
- 確保所有人可以透過 eth.limo 查看  
- 每次更新 CID，即可更新 ENS 上的 contenthash（可自動化）

---

## 🔁 ENS 綁定 CID 的流程（已完成）

1. 在 ENS App 中設定 contenthash  
2. CID 格式需經過 `0xe3...` 編碼  
3. 確認 ENS Resolver 正常  
4. 使用 eth.limo / eth.link 驗證  
5. 更新新的 CID 時，只需再次發送交易更新 contenthash

---

## 🛠 未來可加入的功能

- 自動化更新 ENS contenthash（依文件快照更新）  
- 將 IPFS → ENS 更新流程寫入 systemd 或 cron  
- 將 ENS 當作公開 metadata 的入口  
