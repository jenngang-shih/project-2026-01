<!--
Traceability:
  Source file: docs/problem-statement.md (project root, original combined document)
  Topic: 1 — 主題一：高階 Prompt Chaining (提示詞鏈) 規劃與執行
  Extraction method: split on delimiter pattern `主題*：` (regex: ^主題[一二三四]：)
  Extracted: verbatim, no edits to original content below this header
-->

主題一：高階 Prompt Chaining (提示詞鏈) 規劃與執行
1. 背景 (Background)
[娛樂城] 這個關鍵字是該產業中 SEO 競爭最激烈的關鍵字之一。為了在搜尋引擎中脫穎而出，僅提供「產品、資訊列表或是表面的品牌羅列比較」已不足夠，Google 更偏好具備 Experience (經驗) 的內容。本題要求你設計一個自動化提示詞鏈(Chain of Prompts)，將語意模糊的關鍵字轉化為具備「深度玩家洞察」的文章規劃。請先對以下專有名詞進行研究並建立基本觀念，並歸納關鍵點：
•         Search Intent 與 Micro Search Intent 
•         EEAT 與 YMYL

2. 要求 (Requirements)
本題不考慮單次性的 Zero-shot (零樣本) 或 Few-shot (少樣本) 提示詞，必須以 Prompt Chain (提示詞鏈) 的形式展現以下三個階段：
 
階段 A：微搜尋意圖建模 (Micro-Intent Modeling)
•         輸入：關鍵字 [娛樂城]。
•         任務：分析並產出至少 4 個層次的真實 Micro Search Intent (微搜尋意圖)（例如：針對出金速度的焦慮、特定代理商的信任驗證、不同遊戲 UI 的沉浸感需求等）。
•         Logic (邏輯力) 要求：需有證據的解釋為何選擇這些微意圖，其背後的 SEO 競爭邏輯為何。
 
階段 B：邊緣案例 —— 獨立經驗模擬 (Edge Case: First-hand Experience)
•         任務：針對上述其中一個意圖，設計一個 Prompt Chain 引導 AI 產出具備「玩家試玩情境」的內容段落。
•         要求：內容必須包含不限於如 Sensory Details (感官細節) 與 Objective Critique (客觀評論)。
•         特殊留意點：必須展示如何抑制 AI 產出「作為一個 AI 語言模型...」或過於虛假的誇讚語氣，確保內容看起來像是一位台灣的資深玩家的獨立心得。
 
階段 C：EEAT/YMYL 合規性審核 (Compliance & Safety Audit)
•         任務：建立一個 Self-Correction (自我修正) 提示詞鏈。
•         功能：自動檢核階段 B 的產出是否符合 EEAT/YMYL 原則，同時優化其 Authoritativeness (權威性) 指標。

3. 交付物 (Deliverables)
•  Asked results of A, B, C
•  Iterative Record (迭代紀錄)：完整的對話歷史（請提供如 ChatGPT/Claude/Gemini 的對話分享連結）。
•  Architecture Diagram (架構圖)：使用 Markdown、Mermaid 或相關工具繪製此 Prompt Chain (提示詞鏈) 的資訊流向圖。
•  Rationale (理論依據)：一份簡短的技術說明，描述你如何透過提示詞設計來確保產出符合 EEAT 原則。

4. 評核標準 (Evaluation Criteria)
•  Detail-Oriented (細節重視)：產出的內容是否具備無法輕易被 AI 偽造的「特定細節」。
•  Logical Consistency (邏輯一致性)：從意圖分析到最終成文，邏輯鏈條是否緊密扣合。
•  Independent Thinking (獨立思考能力)：能識別並修正 AI 常見的邏輯漏洞（如過度正向的廢話）。
