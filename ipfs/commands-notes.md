# IPFS 常用指令備忘錄（草稿）

這裡整理在節點上常用的 IPFS 指令，方便之後查。


# 啟動 daemon
ipfs daemon

# 新增檔案並取得 CID
ipfs add <file>

# 將 CID 固定（避免被 GC 掃掉）
ipfs pin add <CID>

# 列出已 pin 的內容
ipfs pin ls

# 查看節點資訊
ipfs id

# 查看 repo 使用的空間
ipfs repo stat
