# 貢獻指南

感謝你有興趣為 Vanscoding Skills 做出貢獻！本文件說明如何貢獻到此專案。

## 如何貢獻

### 報告錯誤（Bug Report）

如果你發現了錯誤，請提交一個 Issue，包含：

- 錯誤的詳細描述
- 重現步驟
- 預期行為 vs 實際行為
- 使用的技能和環境資訊

### 提交功能建議（Feature Request）

如果你有新功能的想法，請提交 Issue，說明：

- 功能的目的
- 使用場景
- 預期的實現方式

### 提交代碼（Pull Request）

1. Fork 此倉庫
2. 建立你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改動 (`git commit -m '新增某個功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

## 代碼規範

### 檔案和資料夾命名

- 使用小寫字母和連字符號（kebab-case）命名資料夾
- 例如：`google-email`、`agent-soul-crafter`

### Python 代碼

- 遵循 PEP 8 規範
- 使用 type hints（型別提示）
- 添加必要的文件說明和註解

### 文件格式

- 技能文件必須包含 `SKILL.md`
- 使用 Markdown 格式
- 附加文件應該放在適當的子資料夾中

## 技能貢獻指南

如果你想貢獻一個新技能：

1. **建立資料夾**
   ```
   Documents/ 或 Productivity/
   └── your-skill-name/
       ├── SKILL.md
       ├── scripts/
       ├── LICENSE.txt
       └── README.md (可選)
   ```

2. **撰寫 SKILL.md**
   
   SKILL.md 應該包含：
   - 技能的名稱和描述
   - 何時使用此技能
   - 詳細的使用指南
   - 代碼示例
   - 常見問題解答

3. **添加指令碼和工具**
   - 將實用工具放在 `scripts/` 資料夾中
   - 添加適當的文件說明

4. **授權**
   - 檢查是否需要添加 LICENSE.txt
   - 確保所有第三方代碼的授權相容

## 提交訊息格式

使用繁體中文撰寫提交訊息，遵循以下格式：

```
簡短摘要（50 字以內）

詳細說明（72 字換一行）：
- 第一個重點
- 第二個重點
- 等等

如果是 Issue 相關，添加：
Fixes #123
```

## 風格指南

- 在文件中使用繁體中文進行說明
- 保持代碼的一致性
- 使用有意義的變數名稱
- 添加必要的錯誤處理

## 社區互動

- 尊重他人的意見和想法
- 提供建設性的反饋
- 幫助新貢獻者

## 問題和討論

- 對於一般性問題，請使用 Discussions
- 對於錯誤，請提交 Issue
- 對於大型改動，請先開啟 Issue 進行討論

## 授權

通過貢獻此專案，你同意你的貢獻將根據 LICENSE 檔案進行授權。

感謝你的貢獻！🎉
