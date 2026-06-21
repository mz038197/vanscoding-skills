# PPT 投影片對照（MD → pptx）

腳本 `build_capstone_ppt.py` 依此對照產生 `專題報告.pptx`。手動調整時可參考。

| 投影片 | 標題 | 內容來源 |
|--------|------|----------|
| 1 | 封面 | 專題名稱、組員、日期 |
| 2 | 專題介紹 | MD §1 bullet |
| 3 | 學校 Server 環境 | 短段 + **server-topology.png** 全幅 |
| 4 | 系統概覽 | **project-architecture.png** + §2 精簡 bullet |
| 5 | 成果 | §3 bullet |
| 6 | 創新／亮點 | §4 bullet |
| 7 | 技術含量 | §5 bullet |
| 8+ | Demo | 每張 **demo-XX.png** 一頁，標題用自訂頁名 |

## 版式預設

- 無校徽、無學校 logo
- 標題 28pt、內文 18pt（腳本預設）
- 圖片置中，高度約投影片高度 55%

## 指令

```bash
python "<skill>/scripts/build_capstone_ppt.py" --report-dir report
```

需 `python-pptx`：`uv pip install python-pptx`
