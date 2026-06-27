# 出題避重（agent 內部）

## 狀態檔

路徑：**`mock-exam/.fadou-exam-used.json`**（工作區內；建議 gitignore）

```json
{
  "version": 1,
  "pools": {
    "ethics": { "used": ["1-1"], "last_reset": null },
    "python": { "used": [], "last_reset": null },
    "theory": { "used": [], "last_reset": null },
    "tech": { "used": [], "last_reset": null },
    "drill:4.4-生成式AI": { "used": ["4-120"], "last_reset": null }
  },
  "sessions": [],
  "updated_at": "2026-06-23T12:00:00"
}
```

- **內部題號**：題庫表格第一欄（`1-1`、`2-14`…）；**不向學生透露**
- **模擬考四池**：`ethics` / `python` / `theory` / `tech`（各 10/10/10/20）
- **專項池**：`drill:<slug>`，`slug` = scope 去空白、全形空格、`/`→`-`

## 模擬考 SOP

1. 確保 `mock-exam/` 存在
2. 建議題號：

```bash
python "<skill-root>/scripts/suggest_bank_ids.py" --mode mock --history mock-exam/.fadou-exam-used.json
```

3. 依 stdout 的 `bankIds` / `byCategory` 從題庫組 50 題 → `questions.json`（含 `_meta`）
4. `build_mock_exam.py … --open`
5. 記錄已出題：

```bash
python "<skill-root>/scripts/record_used_questions.py" questions.json --history mock-exam/.fadou-exam-used.json
```

6. 若 `poolResets` 非空 → 學生可見：「部分範圍題目已練過一輪，這次是新的一批。」

## 專項 SOP

```bash
python "<skill-root>/scripts/suggest_bank_ids.py" --mode drill --scope "4.4 生成式 AI" --count 5 --history mock-exam/.fadou-exam-used.json
```

出 5 題後：

```bash
python "<skill-root>/scripts/record_used_questions.py" --bank-ids 4-120,4-121,... --mode drill --scope "4.4 生成式 AI" --history mock-exam/.fadou-exam-used.json
```

## questions.json `_meta`

```json
{
  "_meta": {
    "mode": "mock",
    "scope": null,
    "bankIds": ["1-1", "2-14", "..."]
  }
}
```

`build_mock_exam.py` 嵌入 HTML 前會移除 `_meta`。

## 題池用盡

`suggest_bank_ids.py` 某池可用題不足 → 該次從全池重抽（`poolResets` 回報）；`record_used_questions.py` 仍追加 used。
