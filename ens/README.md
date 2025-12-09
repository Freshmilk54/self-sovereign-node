# ENS 設定與 CID 綁定流程

本資料夾紀錄我在 self-sovereign-node 中使用 ENS 的方式，以及將 IPFS CID 綁定到 ENS，使其可以透過 eth.limo / eth.link gateway 對外展示。

---

## 🌐 ENS Domain Used

目前使用的 ENS 名稱：
dk45dola.eth

對外瀏覽頁面（eth.limo）：
https://dk45dola.eth.limo/

## 📦 功能摘要

- 租用 ENS 網域  
- 將 IPFS CID 綁定到 ENS（設定 contenthash）  
- 確保所有人可以透過 eth.limo 查看  


## 🛠 未來可加入的功能

- 自動化更新 ENS contenthash（依文件快照更新）  
- 將 IPFS → ENS 更新流程寫入 systemd 或 cron  
- 將 ENS 當作公開 metadata 的入口  
