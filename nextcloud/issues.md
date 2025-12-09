# Nextcloud 問題與解法紀錄（草稿）

這裡用來紀錄在 Pi 上跑 Nextcloud 時遇到的各種問題與解法，  
包含效能、容量、權限、網路等。

---

## 1. 磁碟空間不足 / data 變很肥

- 可能原因：
  - 垃圾桶未清理
  - 舊版本檔案堆積
  - 日誌檔過大
- 之後可以在這裡補：
  - 使用 `occ files:cleanup`、`trashbin:cleanup` 的紀錄
  - 實際清理前後的 `df -h` 差異

---

## 2. 上傳大小受限制

- 方向：
  - PHP `upload_max_filesize` / `post_max_size`
  - Web server 本身的上傳限制
- 待補實際設定值與檔案位置

---

## 3. 權限問題（Can't write into data directory）

- 可能原因：
  - data 目錄 owner / group 設錯
  - 掛載磁碟沒有給 www-data 權限
- 待補：實際 `chown` / `chmod` 指令

---

## 4. 其他踩雷

之後你遇到問題時，可以直接在這裡開新小節，  
方便未來自己回頭查，也讓這個 repo 更有「真實實戰紀錄」的感覺。
