# 公開資料夾與 IPFS 同步設計

這份文件說明：  
我在 Nextcloud 裡面建立一個「專用公開資料夾」，  
搭配 `/usr/local/bin/nextcloud_ipfs_sync.sh` 腳本，  
自動把該資料夾裡的檔案上傳到 IPFS 並 pin 起來。

---

## 📁 資料夾結構概念

Nextcloud 中會有一個特定目錄（路徑依實際使用者而定），例如：

- `public/`

用途：

- 使用者把想要「公開＋去中心化備份」的檔案丟進這個資料夾  
- 其他 Nextcloud 資料仍然是私有的，不會被自動上 IPFS

---

## 🔁 同步腳本：`/usr/local/bin/nextcloud_ipfs_sync.sh`

這個腳本會做的事情：

1. 掃描 Nextcloud 的公開資料夾
2. 把新檔案或變更過的檔案丟給 `ipfs add`
3. 取得對應的 CID
4. 對每個 CID 執行 `ipfs pin add`


實際腳本放在：

- `ipfs/` 資料夾（待新增 `nextcloud_ipfs_sync.sh` 與說明）

---

## 🎯 設計目的

- Nextcloud 管「可修改、可同步」的日常檔案
- IPFS 管「不可變、可長期保存」的內容雜湊
- 公開資料夾充當兩者之間的橋樑

