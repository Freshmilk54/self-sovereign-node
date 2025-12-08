# WireGuard Gateway 筆記（Pi 當 VPN 出口）

這裡紀錄我讓 Raspberry Pi 變成 WireGuard client 的「網路出口（Gateway）」時的設定與踩雷。

## 🎯 目標

- Client（筆電 / 手機）連到 Pi 的 WireGuard 之後：
  - 能連到 Pi 內網服務（Nextcloud、控制台等）
  - 也可以「經由 Pi 上網」

## 🔧 Pi 端設定重點

- 開啟 IPv4 轉送：
  - 編輯 `/etc/sysctl.conf` ：
  -  加入
    ```
    net.ipv4.ip_forward=1
    ```
    
- WireGuard `AllowedIPs` 設定：
  - 內網：`10.66.66.0/24`
  - 全流量走 VPN：`0.0.0.0/0`

## 🧪 測試方式

- `ping 10.66.66.1` 確認可以打到 Pi  
- `curl ifconfig.me` 看對外 IP 是否變成家裡 / Pi 所在網路  


## 📝 備註 (未完)

- 家中 Wi-Fi
  記得要開NAT導向，將51820的UDP轉到 Server的ip這樣才會正式通。
  
- 公共 Wi-Fi
  有些公用網路會把UDP關起來，在這情況下，WireGuard會失效。
  
- 手機熱點時的行為（雙重 NAT）
  
- DNS 設定對瀏覽速度的影響  
