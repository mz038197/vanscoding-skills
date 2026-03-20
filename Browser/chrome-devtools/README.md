# Chrome DevTools MCP（本庫技能）

本目錄提供 **Chrome DevTools MCP** 相關的 Agent 技能定義：透過 MCP 使用 Chrome DevTools 除錯、自動化瀏覽、分析效能與檢視網路請求。

## 本目錄檔案

| 檔案 | 說明 |
|------|------|
| [SKILL.md](./SKILL.md) | 技能說明、工作流程與工具選擇（給 AI / Cursor 使用） |

## 安裝與上游專案

- **官方倉庫與說明**：[ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- **CLI 參考**：於 MCP 設定中可搭配 `npx chrome-devtools-mcp@latest --help` 調整啟動參數（例如瀏覽器 profile）。

## 補充資源

- **Chrome DevTools 文件**：[developer.chrome.com/docs/devtools](https://developer.chrome.com/docs/devtools)
- **DevTools AI 輔助**：[AI assistance](https://developer.chrome.com/docs/devtools/ai-assistance)
- **啟動或連線錯誤**：[上游疑難排解](https://github.com/ChromeDevTools/chrome-devtools-mcp/blob/main/docs/troubleshooting.md)

## 注意

使用 **`--slim` 模式**的 MCP 設定時，不適用本技能（見 `SKILL.md` 開頭說明）。
