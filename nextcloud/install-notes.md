# Nextcloud 安裝與部署筆記（草稿）

這裡紀錄我在 Raspberry Pi 上安裝與維護 Nextcloud 的方式，  

---

## 🖥 環境概況

- 硬體：Raspberry Pi 3
- OS：Raspberry Pi OS Debian
- Web server： Apache
- PHP：<版本>
- DB：MariaDB 

（之後想到再補

---

## 📦 安裝流程（框架）


1. 安裝系統與基本更新  
2. 安裝 Apache、PHP 以及必要模組（php-mysql、php-gd、php-xml 等）  
3. 安裝 MariaDB，建立 Nextcloud 專用資料庫與帳號  
4. 下載並部署 Nextcloud 原始碼到 `/var/www/nextcloud`  
5. 設定檔案權限（www-data / 755 / 750 等）  
6. 設定 Apache VirtualHost，指向 `/var/www/nextcloud`  
7. 透過瀏覽器進行初次安裝流程  
8. 調整 `config.php`（對照 `config-example.php`）

---

## 🗄️ MariaDB 資料庫設定（範例）

> 實際帳號密碼請改成自己的，這裡只示範結構。

```sql
CREATE DATABASE nextcloud CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
CREATE USER 'nextcloud'@'localhost' IDENTIFIED BY '<DB_PASSWORD>';
GRANT ALL PRIVILEGES ON nextcloud.* TO 'nextcloud'@'localhost';
FLUSH PRIVILEGES;

對應到 config-example.php
'dbname' => 'nextcloud'
'dbuser' => '<DB_USERNAME>'
'dbpassword' => '<DB_PASSWORD>'

```markdown
## 🌐 Apache VirtualHost 設定（範例）

```apache
<VirtualHost *:80>
    ServerName <YOUR_PUBLIC_DOMAIN>    #改成自己的網域或IP
    DocumentRoot /var/www/nextcloud

    <Directory /var/www/nextcloud>
        Require all granted
        AllowOverride All
        Options FollowSymLinks MultiViews
    </Directory>

    ErrorLog ${APACHE_LOG_DIR}/nextcloud_error.log
    CustomLog ${APACHE_LOG_DIR}/nextcloud_access.log combined
</VirtualHost>



## 🗃 儲存空間與資料目錄

- 資料目錄：`/srv/nextcloud-data`（之後補） 

---

## 🔁 升級與維護

- 如何停服務、執行 `occ upgrade`（之後補）  
- 備份策略（DB + data）  
- Log 存放位置  

---

## 🧪 測試清單（未來可用）

- 新增帳號 / 登入正常
- 手機 App 可以連線
- 檔案上傳 / 下載沒問題
- 公開資料夾 + IPFS 同步流程正常觸發
