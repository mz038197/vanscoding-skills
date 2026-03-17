---
name: user-md-guide
description: >-
  引導初次使用者建構給自己 agent 使用的 USER.md，融合「人本敘事」與「結構化偏好」兩種風格，
  產出單一統一的設定檔。當使用者要建立 USER.md、寫給 AI 用的個人檔案、或問「怎麼讓 agent 更懂我」時使用此 skill。
---

# USER.md 建構引導 — 給 Agent 用的個人檔案

本 skill 協助初次使用者一步步完成 **USER.md**，讓 Cursor、nanobot 或其他 agent 能根據「你是誰、你的偏好、你的情境」提供更個人化的協助。採用**融合風格**：兼顧「人本敘事」（About your human）與「結構化偏好」（溝通風格、技術程度、工作情境）。

## 何時使用本引導

- 第一次要為工作區或 agent 建立 USER.md
- 想統一「給 AI 看的個人設定」、避免多套格式並存
- 不確定該寫「輕鬆介紹自己」還是「勾選偏好」——本引導兩者都涵蓋

## USER.md 是什麼

`USER.md` 是給 **agent 讀的個人檔案**，描述「正在協助的這個人」：稱呼、時區、溝通偏好、工作情境、地雷與笑點等。Agent 會在 bootstrap 或個人化時讀取，用來調整語氣、長度與建議方向。本引導產出的格式同時適用 Cursor 系工具與 nanobot 等結構化解析。

---

## 撰寫流程（依序進行）

### 步驟 1：確認檔案位置與標題

- **路徑**：工作區根目錄的 `USER.md`，或專案/環境約定位置（例如 `~/.nanobot/workspace/USER.md` 若使用 nanobot）。
- **標題**：建議使用 `# USER.md — About Your Human` 或 `# 給 Agent 的個人檔案`，讓 agent 一眼辨識。

先詢問：「這份 USER.md 會放在哪個專案或目錄？希望標題用英文還是中文？」

---

### 步驟 2：填寫「基本資訊」（必填）

對應融合版區塊 **Basic Information**。逐項引導填寫，必要時給範例：

| 欄位 | 說明 | 範例 |
|------|------|------|
| **Name** | 真實名字或暱稱 | 小明、Wei |
| **What to call them** | Agent 該怎麼稱呼你 | 「請叫我小華」 |
| **Pronouns** | 代名詞（選填） | they/them、他/她 |
| **Timezone** | 時區 | UTC+8、Asia/Taipei |
| **Language** | 偏好語言 | 繁體中文、English |
| **Notes** | 一兩句備註 | 「常熬夜，下午才回訊息」 |

**引導方式**：一次問 1～2 個欄位，避免一次丟整張表。可問：「你希望 agent 怎麼稱呼你？」「你主要在哪個時區活動？」

---

### 步驟 3：選擇「偏好」（結構化，選填）

對應融合版的 **Preferences**，用勾選讓 agent 知道溝通風格、回答長度與技術程度。向對方說明：「勾選你當下最符合的即可，之後可改。」

- **Communication Style**：Casual / Professional / Technical（可多選或單選，依實作而定）
- **Response Length**：Brief and concise / Detailed explanations / Adaptive based on question
- **Technical Level**：Beginner / Intermediate / Expert

**引導方式**：問「你比較喜歡簡短回答還是詳細說明？」「你覺得自己目前是初學、中階還是進階？」再代為轉成對應勾選。

---

### 步驟 4：填寫「工作情境」（選填）

對應融合版 **Work Context**：角色、主要專案、常用工具。幫助 agent 在給建議時對齊你的情境。

- **Primary Role**：例如學生、開發者、研究者
- **Main Projects**：目前在做什麼（一兩句或條列）
- **Tools They Use**：常用 IDE、語言、框架

**引導方式**：問「你現在主要身份是什麼？在忙什麼專案？」「平常寫程式用什麼語言或工具？」

---

### 步驟 5：撰寫「Context」（人本敘事，建議填）

對應融合版 **Context**：自由文字，描述「這個人在乎什麼、討厭什麼、什麼會笑」。隨時間更新，不必一次寫完。

- 在乎的事、正在煩惱的
- 地雷（不喜歡的語氣或假設）
- 喜歡的互動方式、笑點或梗

**引導方式**：問「你希望 agent 特別記得什麼關於你的事？」「有什麼地雷或偏好要提醒 agent？」強調「這是給 agent 了解你這個人，不是交作業，可以之後慢慢補。」

---

### 步驟 6：填寫「Special Instructions」與「Topics of Interest」（選填）

- **Special Instructions**：給 agent 的明確行為指示，例如「回答請用繁體中文」「不要假設我有 CLI 經驗」。
- **Topics of Interest**：三兩項你常問或想深入的主題，方便 agent 預判方向。

**引導方式**：問「有沒有你希望 agent 一定遵守的規則？」「你最近常問或想學的主題有哪些？」

---

### 步驟 7：收尾與檢查

1. **存檔**：確認 `USER.md` 在約定路徑、副檔名為 `.md`。
2. **結構檢查**：至少具備「基本資訊」與「Context」或「Preferences」其一；若有 YAML frontmatter，確認格式正確。
3. **用語一致**：若專案已有 AGENTS.md 或其它術語，與 USER.md 用詞一致。

---

## 統一模板（融合兩風格）

引導時可依步驟逐步產出，或最後給對方一份完整範本供複製後自行填寫。以下為融合版結構，含 YAML 與區塊標題。

```markdown
---
summary: "User profile — preferences and context for personalized assistance"
read_when:
  - Bootstrapping a workspace manually
  - Personalizing nanobot or agent behavior
---

# USER.md — About Your Human

_Learn about the person you're helping. Update this as you go._

## Basic Information

- **Name:**
- **What to call them:**
- **Pronouns:** _(optional)_
- **Timezone:** _(e.g. UTC+8)_
- **Language:** _(preferred)_
- **Notes:** _(short note or reminder)_

---

## Preferences

### Communication Style

- [ ] Casual
- [ ] Professional
- [ ] Technical

### Response Length

- [ ] Brief and concise
- [ ] Detailed explanations
- [ ] Adaptive based on question

### Technical Level

- [ ] Beginner
- [ ] Intermediate
- [ ] Expert

---

## Work Context

- **Primary Role:** _(e.g. developer, student, researcher)_
- **Main Projects:** _(what they're working on)_
- **Tools They Use:** _(IDEs, languages, frameworks)_

---

## Context

_(What do they care about? What annoys them? What makes them laugh? Build this over time.)_

---

## Special Instructions

_(Any specific instructions for how the assistant should behave.)_

---

## Topics of Interest

- 
- 
- 

---

*Edit this file to customize behavior. The more you know, the better you can help — and remember to respect the person behind the profile.*
```

---

## 引導時可問的關鍵問題

1. 「這份 USER.md 會放在哪個專案或目錄？標題想用英文還是中文？」
2. 「你希望 agent 怎麼稱呼你？用什麼語言跟你對話？」
3. 「你比較喜歡簡短回答還是詳細說明？你覺得自己目前是初學、中階還是進階？」
4. 「你現在主要身份是什麼？在忙什麼專案？用什麼工具？」
5. 「有沒有你希望 agent 特別記得的事、或一定不要踩的地雷？」
6. 「有沒有希望 agent 一定遵守的規則？最近常問或想學的主題？」

依回答逐段產出對應的 USER.md 內容，並建議貼到約定路徑後再微調。

---

## 總結檢查清單

完成後可協助對方確認：

- [ ] 檔案名為 `USER.md`，位於約定目錄（工作區根目錄或環境指定路徑）
- [ ] 至少具備「基本資訊」與「Context」或「Preferences」其一
- [ ] 若使用 nanobot 或會解析 frontmatter 的工具，已加上 YAML 與 `read_when`
- [ ] 用語與專案／AGENTS.md 一致，長度適中，方便日後維護
