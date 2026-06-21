# Step 6 交件驗收

Agent 在標記「交件完成」前**逐項檢查**（可腳本 + 人工）。任一失敗 → 回到對應步驟。

## 檔案存在

| 路徑 | 必要 |
|------|------|
| `report/專題報告.md` | ✓ |
| `report/專題報告.pptx` | ✓ |
| `report/專題報告.docx` | ✓ |
| `report/project-architecture.mmd` | ✓ |
| `report/assets/server-topology.png` | ✓ |
| `report/assets/project-architecture.png` | ✓ |
| `report/assets/demo-*.png` | ✓ 張數 ≥ 自訂頁數 |

## 內容對齊

- [ ] MD §1–5 與 Step 3c 對齊條列一致（無擅自新增功能）
- [ ] 報告**無** api_key、Router IP／URL
- [ ] 個人架構 Mermaid 節點為白話中文（非 `format_extra_context` 作主標）

## DOCX 圖片（硬性）

執行：

```bash
python "<skill>/scripts/build_capstone_docx.py" --report-dir report --verify-only
```

或 Agent 用 python-docx 讀取 `專題報告.docx` 統計 `inline_shapes` / 圖片關係：

- **至少** 2 + demo 張數（server + 架構 + 各 demo）
- 若只有文字 → **失敗**，依 `docx-fallback.md` 處理，**不得**交件

## 學生可見驗收問句（一次一條）

1. 三份檔 `md / pptx / docx` 都打開了嗎？
2. Word 裡看得到 server 圖、架構圖嗎？
3. 每個自訂頁的 demo 圖都在 Word 附錄嗎？

全部 OK → 「專題報告已完成，可以繳交 `report/` 資料夾。」

## Preflight 紀錄

`report/.capstone-progress.md` 應含：

- 自訂頁清單
- demo 需求張數
- 已完成 step_id
