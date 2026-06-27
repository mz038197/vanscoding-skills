# 網頁模擬考指南（agent 內部）

## 流程

1. Read `references/knowledge/人工智慧工程素養認證-考前須知-上傳版.md`
2. 依 [question-dedup-guide.md](question-dedup-guide.md) 跑 `suggest_bank_ids.py`，從四類題庫組 **50 題**（避待核；推導題改四選一）
3. 寫入工作區 `questions.json`（含 `_meta.bankIds`；見下方 schema）
4. 執行（**必須 `--open`**）：

```bash
python "<skill-root>/scripts/build_mock_exam.py" questions.json -o mock-exam/<YYYYMMDD-HHMM>/ --open
```

5. 記錄已出題：

```bash
python "<skill-root>/scripts/record_used_questions.py" questions.json --history mock-exam/.fadou-exam-used.json
```

6. 回覆學生：「模擬考卷已在瀏覽器開啟。交卷後可看錯題檢討、複製或下載 `.md` 貼回 Cursor。」

**禁止：** 要學生自己開 `index.html`、雙擊檔案、或到資料夾找路徑。

## questions.json schema

```json
{
  "_meta": {
    "mode": "mock",
    "scope": null,
    "bankIds": ["1-1", "2-14"]
  },
  "title": "人工智慧工程素養認證｜模擬考",
  "passScore": 70,
  "sessionId": "20260623-1030",
  "questions": [
    {
      "id": 1,
      "category": "AI 倫理與社會影響",
      "section": "AI 倫理概念理解",
      "stem": "題幹文字",
      "options": { "a": "…", "b": "…", "c": "…", "d": "…" },
      "answer": "a"
    }
  ]
}
```

- `questions` 長度 **50**；`id` 1–50 連續
- `_meta.bankIds` 長度 **50**（Agent 內部；HTML 不含）
- 卷面 JSON **不要**內部題號（如 `2-14`）
- `build_mock_exam.py` 以 `-o` 目錄名注入 `sessionId`

## 配分對照

| id | category |
|----|----------|
| 1–10 | AI 倫理與社會影響 |
| 11–20 | Python 基礎運用 |
| 21–30 | 人工智慧理論知識 |
| 31–50 | 人工智慧技術運用 |

## 輸出目錄

```
mock-exam/
├── .fadou-exam-used.json
└── <timestamp>/
    ├── index.html
    ├── questions.json
    ├── styles.css
    ├── exam.js
    └── README.txt
```

## 學生端行為（exam.js）

| 情境 | 行為 |
|------|------|
| 作答中 F5／關分頁再開 | 恢復草稿（localStorage） |
| 交卷後 F5 | **保留成績與錯題檢討**（sessionStorage） |
| 交卷後關分頁再開 | 空白卷（可重考同卷） |
| **重新測試** | 新一輪同卷；上一輪成績不能用 F5 叫回 |
| 錯題檢討 | 畫面完整題目；可複製／下載 `錯題檢討-<sessionId>.md` |

## `--open` 失敗

改提供 `file:///` 連結；仍禁止「請到資料夾找檔案」。
