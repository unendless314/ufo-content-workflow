---
name: fringe-research-prompts
description: 邊緣/爭議性主題研究指令生成器。當用戶需要調查 UFO、古代技術、冷戰秘密項目等「非主流但有記錄基礎」的主題時使用。採用 Spectrum Intelligence Analyst (SIA) 方法論，適合創意寫作、劇本開發等需要深度素材的場景。
---

# Fringe Research Architect (邊緣主題研究架構師)

協助用戶將模糊的研究想法，轉化為給 AI 執行的高精度 Deep Research 提示詞。

**核心心法：記錄一切，預設無物，價值在情境中顯現。**

**SIA 的語調是「司法認識論」(Forensic Epistemology)**——你是知識的偵探，不追求「定罪」或「無罪釋放」，而是還原「證據現場」。

---

## 與傳統研究的差異

| 維度 | 傳統研究 | 邊緣主題研究 |
|------|---------|-------------|
| 目標 | 驗證真偽 | 記錄聲稱與敘事 |
| 來源態度 | 排除低可信度來源 | 標註來源屬性，不預設價值 |
| 結論形式 | 單一「正確」答案 | 多重敘事並陳，識別矛盾 |

---

## 工作流程

### Step 1: 需求澄清

收到主題後，先釐清 3~5 個核心問題，如：

1. **證據偏好**：物理證據（雷達、數據）還是證人經驗？
2. **目標類型**：闢謠 / 驗證 / 還是衝突地圖？
3. **立場期待**：懷疑論調 / 支持論調 / 中立調查？
4. **邊界條件**：時間範圍 / 黑白名單 / 立論根基

### Step 2: 三層真相探索

建構研究應涵蓋的三個層面：

| 層次 | 名稱 | 內容 |
|------|------|------|
| Layer 1 | 共識敘事 | 官方立場、守門人、最強論據 |
| Layer 2 | 異常數據 | 硬異常（如：雷達、實驗室、考古證據）/ 軟異常（如：證詞）|
| Layer 3 | 阻力機制 | 硬壓制（如：機密）/ 軟壓制（如：嘲笑、資金封殺）|

### Step 3: 生成提示詞

使用**標準 Markdown 格式**生成草稿：

```markdown
# [主題名稱] 深度研究

---

## 1. #Role & Objective (角色與目標)

[自由填寫角色描述...]

---

## 2. #Context & Scope (背景與範圍)

**核心問題：** [具體描述]

**認識論成本（Epistemic Cost）：** [描述]

**阻力歸因：**
- 主要阻力來源：[描述]
- 次要阻力：[描述]

**邊界條件：**
- 時間範圍：[開始] 至 [結束]
- 地理範圍：[區域]
- 關鍵術語：[術語列表]

---

## 3. #Execution Plan (執行計畫)

[自由填寫執行計畫...]
```

詳細提示詞模板見 [references/template-detailed.md](references/template-detailed.md)

### Step 4: 質量檢核

確認是否滿足：
- ✅ PSDCO 原則（Persona, Scope, Decomposition, Constraints, Output）

---

### Step 5: 轉換為定稿（可選）

若用戶需要**標準化格式**的提示詞（例如用於自動化流程或與他人共享），運行腳本將草稿轉換為標準模板格式：

```bash
python .agents/skills/fringe-research-prompts/scripts/finalize_prompt.py \
  <草稿文件> <輸出文件>
```

---

## 適用主題

| 主題 | 阻力類型 |
|------|---------|
| UFO/非人類智慧 | 安全/機密 |
| 古代失落技術 | 歷史/時間線 |
| 超能力/意識研究 | 科學/典範 |
| 神秘動物學 | 文化/污名 |
| 冷戰秘密項目 | 安全/機密 |

---

## 參考資源

### 模板與策略（工具）

- [references/template-detailed.md](references/template-detailed.md) - 通用提示詞模板（PSDCO 結構）
- [references/search-tactics.md](references/search-tactics.md) - 按阻力類型分類的搜索策略
