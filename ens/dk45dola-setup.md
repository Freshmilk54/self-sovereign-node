# dk45dola.eth 設定紀錄：ENS + IPFS + eth.limo

這份文件紀錄我如何把：

- ENS 名稱：`dk45dola.eth`
- IPFS CID：<SOME_CID>
- eth.limo gateway：`https://dk45dola.eth.limo/`

串在一起，讓瀏覽器可以透過 ENS 直接顯示 IPFS 內容。

---

## 🧩 整體概念

資料流概念：

1. 先在 ENS 上註冊 `dk45dola.eth`  
    在 ENS 官方網站進行
    搜尋 dk45dola.eth 是否可用，選擇註冊年限
    使用錢包（MetaMask）在對應網路上送出註冊交易
    完成後，dk45dola.eth 會歸屬於我的地址
2. 在 ENS 設定中，將 `contenthash` 指向某個 IPFS CID  
    在「Records」中找到 Content hash 欄位
    填入對應的 IPFS CID
    使用第三方 gateway（例如 `eth.limo`）  
    最後形成對外網址：
     https://dk45dola.eth.limo/

