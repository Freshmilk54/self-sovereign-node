#!/bin/bash

#!/bin/bash
# Nextcloud → IPFS 選擇性同步（附刪除/搬移處理與除抖）
# 作者：你 + 你那位沒耐心但還是幫你收尾的機器朋友(謝謝你~)


set -euo pipefail

##### 可調區 #####
WATCH_DIR="<NEXTCLOUD_PUBLIC_DIR>"       # 你要同步的位址

# 使用者家目錄與檔案

USER_HOME="$HOME"
LOG_FILE="$USER_HOME/ipfs_sync.log"      # 同步流水帳
MAP_FILE="$USER_HOME/.ipfs_map.tsv"      # 路徑\tCID 對照表（拿來 unpin）
IPFS_BIN="/usr/local/bin/ipfs"           # which ipfs 看一下
IPFS_PATH_DEFAULT="$USER_HOME/.ipfs"     # 你的 ipfs repo
DEBOUNCE_SEC=5                           # 同一路徑事件在 5 秒內只處理一次

##### 可調區結束 #####

# 確保檔案存在
touch "$LOG_FILE" "$MAP_FILE"

# 若外部沒帶 IPFS_PATH，就用你的預設
export IPFS_PATH="${IPFS_PATH:-$IPFS_PATH_DEFAULT}"

# 除抖資料結構（路徑 -> 最後處理時間）
declare -A LAST_SEEN

# 小工具：log
log() { echo "$(date '+%F %T') | $*" >> "$LOG_FILE"; }

# 小工具：對照表
get_cid() { awk -v k="$1" -F'\t' '$1==k{print $2}' "$MAP_FILE" | tail -n1; }
set_map() {
  # 刪舊加新，避免一條路徑有多條紀錄
  grep -v -F "$1"$'\t' "$MAP_FILE" > "${MAP_FILE}.tmp" 2>/dev/null || true
  mv "${MAP_FILE}.tmp" "$MAP_FILE"
  echo -e "$1\t$2" >> "$MAP_FILE"
}
del_map() {
  grep -v -F "$1"$'\t' "$MAP_FILE" > "${MAP_FILE}.tmp" 2>/dev/null || true
  mv "${MAP_FILE}.tmp" "$MAP_FILE"
}

# 忽略 Nextcloud/編輯器暫存垃圾
is_temp() {
  local name="$1"
  [[ "$name" == *.part ]]        && return 0
  [[ "$name" == *ocTransferId* ]]&& return 0
  [[ "$name" == *.swp ]]         && return 0
  [[ "$name" == ._* ]]           && return 0
  [[ "$name" == .DS_Store ]]     && return 0
  return 1
}

# 安全 pin（只輸出 CID），失敗會寫 log 但不炸掉 while
safe_pin() {
  local file="$1"
  local cid
  if cid="$("$IPFS_BIN" add -Q --pin=true "$file" 2>>"$LOG_FILE")"; then
    echo "$cid"
  else
    log "ERROR | PIN_FAIL | $file"
    echo ""
  fi
}

# 安全 unpin（不會因為已不在而炸掉）
safe_unpin() {
  local cid="$1"
  "$IPFS_BIN" pin rm "$cid" >>"$LOG_FILE" 2>&1 || true
}

log "===== watcher start ====="
log "WATCH_DIR=$WATCH_DIR | IPFS_PATH=$IPFS_PATH"

# 監控新增/完成寫入/屬性變更/搬入 + 刪除/搬出
# 註：Nextcloud 上傳通常是 tmp → rename，所以 moved_to 最關鍵


inotifywait -m -r \
  -e close_write,create,attrib,moved_to,move_self,delete,moved_from \
  --format '%w%f|%e' "$WATCH_DIR" \
| while IFS='|' read -r FILE EVT; do
    NAME="$(basename "$FILE")"

    # 除抖：同一路徑 5 秒內只處理一次，避免多事件轟炸
    now="$(date +%s)"
    if [[ -n "${LAST_SEEN[$FILE]:-}" ]] && (( now - LAST_SEEN[$FILE] < DEBOUNCE_SEC )); then
      continue
    fi
    LAST_SEEN[$FILE]=$now

    # 忽略暫存檔
    if is_temp "$NAME"; then
      log "SKIP  | $EVT | $FILE"
      continue
    fi

    # 刪除/搬出：unpin 舊 CID
    if [[ "$EVT" == *DELETE* ]] || [[ "$EVT" == *MOVED_FROM* ]]; then
      old_cid="$(get_cid "$FILE")"
      if [[ -n "$old_cid" ]]; then
        safe_unpin "$old_cid"
        del_map "$FILE"
        log "UNPIN | $EVT | $FILE | CID: $old_cid"
      else
        log "UNPIN | $EVT | $FILE | CID: <unknown>"
      fi
      continue
    fi

    # 新增/寫入完成/搬入：pin 新 CID
    if [[ -f "$FILE" ]]; then
      new_cid="$(safe_pin "$FILE")"
      if [[ -n "$new_cid" ]]; then
        set_map "$FILE" "$new_cid"
        log "PIN   | $EVT | $FILE | CID: $new_cid"
      fi
    else
      # 目錄或其他型態，不處理
      log "INFO  | $EVT | non-regular | $FILE"
    fi
  done
