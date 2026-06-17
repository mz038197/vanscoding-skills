# CLI 工具模式（繁中版）

預設 Webwright 執行（`/webwright:run`、一般 prompt）產出**一次性** `final_script.py`。**CLI 工具模式**（`/webwright:craft`）則產出**可參數化、可重用**的 CLI：同一腳本日後可用不同參數重跑。

任務前須完成 `SKILL.md` 的 **Setup**。瀏覽器預設 **headless Chromium**；必要時 fallback Firefox（見 `playwright_patterns.md`）。

## 何時使用

- 使用者輸入 `/webwright:craft …`，或
- 使用者要求「參數化、可重用、做成 CLI、換不同日期/地點再跑」等。

否則使用預設一次性模式。

## `plan.md` — 新增 `# Parameters`

除 `# Critical Points` 外，列出所有可能變更的條件：

```markdown
# Task
<任務原文>

# Parameters
| name    | type | source phrase from task | default     | allowed / format        |
|---------|------|-------------------------|-------------|-------------------------|
| <arg_a> | str  | "..."                   | "<value>"   | <format / allowed set>  |

# Critical Points
- [ ] CP1: ...
```

規則：

- `# Parameters` 每一列須對應函式參數與 `argparse --flag`（default 如表）。
- 網站固定項（起始 URL、selector 策略）**不是**參數。
- 無參數執行 `python final_script.py` 須重現原任務。
- Critical Points 仍是驗證契約。

## `final_script.py` — 必要結構

1. **一個可重用函式**（命名反映任務領域）。
2. **Google 風格 docstring**（摘要、`Args:`、`Returns:`）。
3. **`argparse` CLI** 於 `if __name__ == "__main__":`，每個參數對應 `--flag`，default 為本次任務的具體值。
4. **import 時無 side effect**（不啟動瀏覽器、不寫檔、不連網）。
5. **log 第一行**（清空 log 後）：
   ```
   step 0 params: arg_a=<value> arg_b=<value>
   ```
6. 與預設模式相同 instrumentation：viewport 1280×1800，headless 本機 **Chromium**（必要時 Firefox），禁止 `full_page=True`；截圖與最終資料寫入 run 資料夾。

## 驗證（取代 `self_reflection`）

除一般 CP 驗證外，CLI 模式還須：

1. **無參數重現任務** — 在 `final_runs/run_<id>/` 執行：
   ```powershell
   uv run python final_script.py
   ```
2. **Import 安全 smoke test** — 另開 process import 模組，確認不啟動瀏覽器。
3. **（可選）** 以不同參數再跑一輪，證明參數化有效。
4. **顯示 `--help`** — 讓使用者知道如何帶參數重跑。

## 完成門檻（CLI 模式）

僅當以下**全部**成立：

1. `plan.md` 含 `# Parameters` 與 `# Critical Points`。
2. `final_script.py` 有唯一可重用函式與完整 `Args:` docstring。
3. 每個參數對應函式參數與 `--flag`。
4. Import smoke test 通過。
5. 無參數執行重現任務；所有 CP 有證據。
6. log 含 `step 0 params: ...`。
7. 使用者已看到最終資料與 `--help`。

任一不成立 → 修正腳本（保持 CLI 結構）→ 在 `run_<id+1>/` 重跑。
