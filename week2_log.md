\# Week 2 tool-use 紀錄



\## 第一次 API 回應

\- name: http\_get

\- arguments:{\\"url\\":\\"https://example.com\\"}

\- tool\_call id: "call-046b5ea0-a886-40bb-8b5e-49feae0eb6be"



\## 工具執行

\- 執行的函式：http\_get()

\- status\_code: 200

\- body\_summary: "<!doctype html><html lang=en><head><meta charset=utf-8><link rel=icon href=data:,><meta name=viewport content=\\"width=dev"



\## 第二次 API 請求

\- 回填的訊息 role: "tool"

\- tool\_call\_id: "call-046b5ea0-a886-40bb-8b5e-49feae0eb6be"



\## 第二次 API 回應

\- choices\[0].message.content: 抓取成功（HTTP 200），我看到的是 example.com 的標準示範頁面，包含一個標題為「Example Domain」的主段落，說明此頁面僅供文件用途，並附上一個指向 moreinfo 連結。



\## 對應講義四列表格

| 步驟 | 模型建議 | 程式實際執行 |

|---|---|---|

| 第一次 API 回應 | name: http\_get, arguments: {\\"url\\":\\"https://example.com\\"} | 尚未執行；只收到建議 |

| 工具執行 | 無 | status\_code: 200, body\_summary: "<!doctype html><html lang=en><head><meta charset=utf-8><link rel=icon href=data:,><meta name=viewport content=\\"width=dev" |

| 第二次 API 請求 | 無 | tool\_call id: "call-046b5ea0-a886-40bb-8b5e-49feae0eb6be" |

| 第二次 API 回應 | 無 | choices\[0].message.content: 抓取成功（HTTP 200），我看到的是 example.com 的標準示範頁面，包含一個標題為「Example Domain」的主段落，說明此頁面僅供文件用途，並附上一個指向 moreinfo 連結。 |

