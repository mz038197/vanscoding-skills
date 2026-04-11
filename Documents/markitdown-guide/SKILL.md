---
name: markitdown-guide
description: Microsoft MarkItDown — convert PDF, PPTX, DOCX, XLSX, images, audio, HTML, etc. to Markdown for LLM pipelines. Covers CLI/Python API, optional extras [pdf,docx,pptx], PPTX embedded images via LLM description and markitdown-ocr plugin, Document Intelligence, plugins. Use when the user mentions markitdown, MarkItDown, 轉成 Markdown, PPTX 圖片轉文字, office 轉 md, or microsoft/markitdown.
---

# Microsoft MarkItDown 使用指南

協助正確回答與實作 [microsoft/markitdown](https://github.com/microsoft/markitdown) 相關問題。官方定位：輕量工具，把多種檔案轉成 **Markdown**，供 LLM 與文字分析管線使用；目標是結構與內容可讀，**不是**高保真人類排版轉檔。

## 何時讀取此 skill

- 使用者問 MarkItDown 安裝、格式支援、CLI／Python API
- 問 **PPTX（或 DOCX 等）裡的圖片** 會不會被處理、如何處理
- 要比較 `markitdown[all]` 與各 optional extra、或 MCP／外掛

## 環境需求

- **Python 3.10+**（README 建議用 venv／uv／conda）
- 安裝：`pip install 'markitdown[all]'` 可還原舊版「一次裝齊」行為；亦可只裝子集，例如：  
  `pip install 'markitdown[pdf,docx,pptx]'`

## PPTX 與「圖片」— 必須區分兩種能力

### 1. 內建：用 LLM 做「圖片描述」（image description）

README 的 Python API 明寫：若要使用 **Large Language Models 做圖片描述**，目前 **僅適用於 `pptx` 與一般圖片檔**（*currently only for pptx and image files*）。  
做法：建立 `MarkItDown` 時傳入 `llm_client`、`llm_model`，可選 `llm_prompt`。

要點：

- **不是**預設就會「看懂」投影片裡每一張圖；需自行提供相容的 LLM client（例如 OpenAI 相容 API）。
- 與「把簡報文字與結構轉成 Markdown」是不同層次的能力。

### 2. 外掛：`markitdown-ocr`（嵌入圖片上的文字／OCR）

README 的 **markitdown-ocr** 小節：此外掛為 **PDF、DOCX、PPTX、XLSX** 等 converter 增加 OCR，從**嵌入圖片**擷取文字，使用 **LLM Vision**（同樣沿用 `llm_client` / `llm_model` 模式），**不需**額外傳統 ML 函式庫或二進位依賴。

- 安裝：`pip install markitdown-ocr`，並安裝 `openai` 或其他 OpenAI 相容 client。
- 使用：`MarkItDown(enable_plugins=True, llm_client=..., llm_model=...)` 後再 `convert(...)`。
- 若**未**提供 `llm_client`，外掛仍會載入，但 OCR **會靜默略過**，退回一般內建轉換。

回答「PPTX 裡的圖片會不會處理」時，應同時說明：**一般轉 Markdown** 與 **LLM 圖片描述**、**OCR 外掛** 三者的差異，避免過度承諾預設行為。

## CLI 速查

```bash
markitdown path-to-file.pdf > document.md
markitdown path-to-file.pdf -o document.md
cat path-to-file.pdf | markitdown
markitdown --list-plugins
markitdown --use-plugins path-to-file.pdf
```

Azure Document Intelligence：CLI 支援 `-d` 與 endpoint 等參數（詳見官方 README）。

## Python API 速查

```python
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)
result = md.convert("test.xlsx")
print(result.text_content)
```

Document Intelligence：`MarkItDown(docintel_endpoint="...")`。  
圖片描述（pptx／圖檔）：`MarkItDown(llm_client=client, llm_model="gpt-4o", llm_prompt="...")`。

## Optional dependency 群組（README 列舉）

記得向使用者提到：可精簡安裝，不必永遠 `[all]`。

- `[all]`、`[pptx]`、`[docx]`、`[xlsx]`、`[xls]`、`[pdf]`、`[outlook]`、`[az-doc-intel]`、`[audio-transcription]`、`[youtube-transcription]` 等（完整列表以官方 README 為準）。

## 版本 breaking changes（0.0.1 → 0.1.0 起）

若使用者從舊教學複製程式碼失敗，可提醒：

- `convert_stream()` 現需 **binary** file-like（例如 `rb` 或 `io.BytesIO`），不再接受純文字 stream。
- `DocumentConverter` 改為從 **stream** 讀取，**不再**建立暫存路徑檔；自訂 plugin／converter 需跟著改。僅用 `MarkItDown` 類別或 CLI 者通常不受影響。

## 延伸資源

- 主 repo：[https://github.com/microsoft/markitdown](https://github.com/microsoft/markitdown)
- MCP 整合：README 指向 **markitdown-mcp**（另套件）
- 第三方外掛：GitHub 搜尋 hashtag `#markitdown-plugin`；開發範例見 repo 內 `packages/markitdown-sample-plugin`

## 回應使用者時的檢查清單

1. 是否需 `[pptx]` 或 `[all]` 才支援 PowerPoint？
2. 「圖片」是指 **版面截圖式還原** 還是 **文字／語意抽出**？後者需 LLM 或 OCR 外掛。
3. 是否在受限環境（無 API、無外掛）？應降低對圖片內容的預期。
4. 需要最高品質表格／版面時，提醒官方說明：輸出主要給 **文字分析工具**，未必適合給人看的精緻排版。
