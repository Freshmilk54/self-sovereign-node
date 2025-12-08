# 樹莓派節點 & 系統設定

本文件紀錄 self-sovereign-node 專案中，Raspberry Pi 作為主節點時的系統層級設定與安全強化措施。

---

## 🖥 節點角色

- 作為整個自我主權節點的核心主機
- 執行服務：
  - WireGuard VPN
  - Nextcloud
  - IPFS daemon
  - Self-Node 控制台（Flask + Gunicorn + Nginx）
  - 定時上鏈腳本（Arbitrum Sepolia snapshot）

---

## 🔐 安全強化（已實作）

### 1. 防火牆：UFW

目的：只開放必要的服務埠，阻擋其餘流量。

目前策略概念：

- 預設：
  - `deny incoming`
  - `allow outgoing`
- 允許：
  - SSH（只給內網 / 指定來源）
  - WireGuard 連接埠
  - Nginx 反向代理使用的 HTTP/HTTPS（僅內網）
  - IPFS
  - Flask 控制台 

> 詳細規則之後可以整理成：
> `device/ufw-rules.md` 或匯出 `ufw status` 貼在這裡。

---

### 2. 防暴力破解 / DDoS 緩解：Fail2ban

目的：避免 SSH / Web 服務被大量暴力嘗試登入。

設定重點：

- 監控：
  - SSH 登入失敗紀錄
  -（如果有需要）Nginx log
- 規則：
  - 同一 IP 多次登入失敗就 temporary ban
- 搭配 UFW 一起阻擋來源 IP

> 未來可以在本資料夾新增：
> `fail2ban/jail.local`、`filter.d/*.conf` 作為設定範例。

---

### 3. SSH 雙重驗證：Google Authenticator (2FA)

目的：就算 SSH 密碼或金鑰外流，也不會直接被登入。

目前設計：

- 使用 Google Authenticator（PAM 模組）  
- 登入流程：
  1. 輸入帳號 / 密碼（或金鑰）
  2. 額外輸入 TOTP（Google Authenticator 產生的一次性密碼）
- 只對管理帳號啟用，搭配 UFW + Fail2ban 一起使用

> 之後可以在這裡補上：
> - `/etc/pam.d/sshd` 相關設定片段  
> - `/etc/ssh/sshd_config` 中與 2FA 有關的設定  

---

## 🧩 未來可以補的內容

- 系統更新策略（定期 apt upgrade / unattended-upgrades）
- 日誌輪替與 log 保存策略
- systemd 服務設定：
  - WireGuard
  - IPFS
  - 控制台（Flask + Gunicorn）
  - 上鏈腳本（timer / service）
- 簡單威脅模型（例如從：內網、外網、裝置遺失 等角度思考）

這一區主要是把「節點本身的硬體與系統層級設定」集中起來，  
讓整個 self-sovereign-node 不只是功能多，而是有**完整安全面的考量**。
