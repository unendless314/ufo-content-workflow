# UFO/UAP 內容創作工作流 (UFO Content Workflow)

> 本文件為 AI 編碼代理設計，提供專案架構、工作流規範與開發指南。

---

## 專案概述

這是一個 **UFO/UAP（不明異常現象）主題的內容創作管理工作流系統**。專案採用結構化的選題管理與 AI 輔助研究流程，支援多平台內容創作（YouTube、Substack、Twitter/X、Podcast 等）。

### 核心特性

- **選題追蹤系統**：基於 YAML 的選題庫管理，支援優先級、狀態與平台規劃
- **AI 研究技能**：內建 Deep Research 與 Fringe Research 提示詞生成器
- **分階段工作流**：從研究、草稿、資產到發布的標準化流程
- **三層真相探索方法論**：專為邊緣/爭議性主題設計的研究框架

---

## 專案結構

```
ufo-content-workflow/
├── topics.yaml              # 選題總表與元資料配置
│
├── 00-archive/              # 已完成的選題檔案
│   └── t000-{prompt,report}.md
│
├── 01-research/             # 進行中的研究資料
│   # 研究報告、原始資料、訪談記錄
│
├── 02-drafts/               # 內容草稿
│   # 腳本、文章草稿、剪輯腳本
│
├── 03-assets/               # 媒體資產
│   # 圖片、影片、音訊、參考文件
│
├── 04-published/            # 已發布內容
│   # 最終版本與發布連結
│
├── scripts/                 # 工具腳本（AI/人類皆可使用）
│   └── todo.py              # 待辦清單生成工具
│
└── .agents/
    ├── skills/
    │   ├── deep-research-prompts/      # 深度研究提示詞生成器
    │   │   └── SKILL.md
    │   │
    │   └── fringe-research-prompts/    # 邊緣主題研究提示詞生成器
    │       ├── SKILL.md
    │       ├── references/
    │       │   ├── template-detailed.md    # PSDCO 標準模板
    │       │   └── search-tactics.md       # 領域特定搜索策略
    │
├── scripts/
│   └── todo.py                     # 待辦清單生成工具（AI/人類皆可使用）
            │   └── archive/                # 舊版模板存檔
            └── scripts/
                └── finalize_prompt.py      # 提示詞定稿工具
```

---

## 技術架構

### 配置管理

**檔案**：`topics.yaml`

選題庫使用 YAML 格式定義，主要欄位：

```yaml
topics:
  - id: t001                    # 選題編號格式: t + 三位數
    title: "..."                # 標題（給觀眾看的敘事性標題）
    research_questions:         # 給 AI 的中性調查問題（3-5 個）
      - "調查..."
      - "分析..."
    status: todo | researching | drafted | published | archived
    priority: p0 | p1 | p2      # P0=立即執行, P1=高優先, P2=待規劃
    type: investigative | analysis | educational | ...
    platforms: [youtube, substack, threads]  # 目標平台
    research_completed: bool
    draft_completed: bool
    published_date: "YYYY-MM-DD" | null
    tags: [immaculate-constellation, pentagon, ...]
    notes: "..."
    files:                      # 檔案關聯（metadata 與內容分離）
      prompt: "01-research/t001-prompt.md"
      report: "01-research/t001-report.md"
      drafts: ["02-drafts/t001-youtube.md", "02-drafts/t001-substack.md"]
      assets: ["03-assets/t001-thumb-01.png"]
```

### AI 技能系統

#### 1. Deep Research Prompts (`deep-research-prompts/SKILL.md`)

**用途**：將研究主題轉化為 AI 可執行的高精度 Deep Research 提示詞

**核心架構**：PSDCO 原則
- **P (Persona)**：定義專家角色
- **S (Scope)**：明確範圍與邊界
- **D (Decomposition)**：分步驟執行計畫
- **C (Constraints)**：資料來源限制（白名單/黑名單）
- **O (Output)**：清晰的輸出格式

**研究策略**：
| 策略 | 適用情境 | 強調重點 |
|------|----------|----------|
| 學術型 | 文獻回顧、理論研究 | 方法論、同行評審期刊 |
| 商業型 | 市場分析、投資評估 | 市場規模、CAGR、競爭對手 |
| 技術型 | 技術評估、架構比較 | GitHub、部署成本、代碼實例 |

#### 2. Fringe Research Prompts (`fringe-research-prompts/SKILL.md`)

**用途**：調查 UFO、古代技術等「非主流但有記錄基礎」的主題

**核心方法論**：Spectrum Intelligence Analyst (SIA)
- **認知映射**：不旨在闢謠或證實，而是映射阻力結構
- **對稱懷疑**：對「官方否認」和「異常聲稱」同等懷疑
- **無懶惰闢謠**：不因主題奇特就否定
- **4-Dimension Attribution**：使用四維度標註每個聲稱

**三層真相探索**：
| 層次 | 名稱 | 內容 |
|------|------|------|
| Layer 1 | 共識敘事 | 官方立場、守門人、最強論據 |
| Layer 2 | 異常數據 | 硬異常（雷達、實驗室）/ 軟異常（證詞）|
| Layer 3 | 阻力機制 | 硬壓制（機密）/ 軟壓制（嘲笑、資金封殺）|

**阻力類型分類**：
- **Type A (安全/機密)**：UFO/UAP、生物武器、黑預算項目
- **Type B (科學/典範)**：超能力、冷核融合、意識研究
- **Type C (歷史/時間線)**：古代失落技術、異常年代測定
- **Type D (文化/污名)**：神秘動物學、通靈現象

### 工具腳本

**`finalize_prompt.py`**：將 AI 生成的草稿提示詞轉換為標準模板格式

```bash
# 使用方法
python .agents/skills/fringe-research-prompts/scripts/finalize_prompt.py \
  <草稿文件> <輸出文件>
```

**功能**：
- 從草稿提取關鍵字段（主題名稱、核心問題、邊界條件等）
- 應用至標準模板
- 保留不可變更的 SIA 核心指令

**`todo.py`**：待辦清單生成器，方便 AI 與人類查看工作狀態

```bash
# 使用方法
python scripts/todo.py [command]

# 可用命令
python scripts/todo.py list              # 列出所有選題
python scripts/todo.py list todo         # 列出待開始的選題
python scripts/todo.py next              # 顯示下一個建議執行的選題
python scripts/todo.py stats             # 顯示統計資訊
python scripts/todo.py research          # 列出需要進行研究的選題
python scripts/todo.py draft             # 列出等待撰寫草稿的選題
python scripts/todo.py overdue           # 列出逾期未完成的 P0 選題
```

**使用時機**：
- AI 開始工作前，執行 `next` 確認優先任務
- 每週回顧時，執行 `stats` 查看整體進度
- 研究階段結束後，執行 `draft` 查看待撰寫的選題

---

## 內容創作工作流

### 標準流程

```
選題規劃 → 研究調查 → 草稿撰寫 → 資產製作 → 發布
    │           │           │           │           │
  topics.yaml  01-research/ 02-drafts/ 03-assets/  04-published/
```

### 目錄使用規範

| 目錄 | 用途 | 命名規範 |
|------|------|----------|
| `00-archive/` | 已完成選題的原始研究檔案 | `{id}-prompt.md`, `{id}-report.md` |
| `01-research/` | 進行中的研究報告、收集資料 | `{id}-research-*.md`, 原始文檔 |
| `02-drafts/` | 內容草稿（腳本、文章） | `{id}-draft-*.md` |
| `03-assets/` | 圖片、影片、音訊、參考 PDF | `{id}-asset-*.{ext}` |
| `04-published/` | 最終發布版本與連結 | `{id}-published.md` |

### 選題狀態轉換

```
todo → researching → drafted → published → archived
         ↓              ↓           ↓
      研究中         撰寫中      已上線
```

---

## 開發指南

### 新增選題

1. 在 `topics.yaml` 新增項目，設定 `id`、`title`、`priority`、`type`
2. 使用 Deep Research 或 Fringe Research Skill 生成研究指令
3. 將研究指令儲存至 `01-research/{id}-prompt.md`
4. 執行研究後，將報告儲存至 `01-research/{id}-report.md`
5. 更新 `topics.yaml` 的 `research_completed: true`

### 建立新技能

若需新增 AI 技能：

1. 在 `.agents/skills/{skill-name}/` 建立目錄
2. 建立 `SKILL.md` 描述工作流程與提示詞模板
3. 參考現有技能結構：
   - 清晰的步驟說明
   - 品質檢核清單
   - 輸出格式規範

### 檔案命名慣例

- **研究檔案**：`{id}-research-{topic}.md`
- **草稿檔案**：`{id}-draft-{platform}.md`
- **資產檔案**：`{id}-asset-{type}-{seq}.{ext}`
  - 例如：`t001-asset-thumbnail-01.png`
- **發布檔案**：`{id}-published.md`（含平台連結）

---

## 4-Dimension Attribution 系統

所有研究來源必須用以下四維度標註：

| 維度 | 選項 | 相關情境 |
|:----:|:----:|:--------:|
| **Proximity**<br>親近性 | Direct / Investigative / Analytical / Commentary | 判斷「到底發生了什麼？」|
| **Timing**<br>時間性 | Contemporaneous / Short-term / Retrospective | 判斷「記憶可靠度」|
| **Vulnerability**<br>風險性 | High-Risk / Med-Risk / Low-Risk / No-Risk | 判斷「動機分析」|
| **Corroborability**<br>可佐證性 | Physical / Multi-Witness / Single-Source / Unverifiable | 判斷「證據強度」|

---

## 語言與風格規範

- **主要語言**：繁體中文
- **專有名詞**：保留英文原文（如 UFO、UAP、NHI）
- **避免詞彙**：「可信」「權威」「偽科學」「陰謀論」
- **改用詞彙**：「官方聲明」「證人證詞」「非主流敘事」

---

## 注意事項

1. **不可修改模板中的固定段落**：`template-detailed.md` 中標記 `[不可變更開始]` 至 `[不可變更結束]` 的 SIA 核心指令
2. **保持 YAML 格式正確**：topics.yaml 的縮排必須一致（使用 2 空格）
3. **研究報告免責聲明**：所有研究旨在反映「社群趨勢與敘事框架」，不對現象真實性背書

---

## 參考資源

- **Deep Research Skill**：`.agents/skills/deep-research-prompts/SKILL.md`
- **Fringe Research Skill**：`.agents/skills/fringe-research-prompts/SKILL.md`
- **詳細模板**：`.agents/skills/fringe-research-prompts/references/template-detailed.md`
- **搜索策略**：`.agents/skills/fringe-research-prompts/references/search-tactics.md`
- **範例研究**：`00-archive/t000-prompt.md`（社群趨勢分析指令）、`00-archive/t000-report.md`（完整研究報告）

---

*最後更新：2026-02-20*

## 更新日誌

- **2026-02-20**: 新增 `research_questions` 欄位與 `files` 檔案關聯結構；建立 `scripts/todo.py` 待辦清單工具
