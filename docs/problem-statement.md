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
 
 

主題二：全端 RAG 系統與 Custom Skill (自定義技能) 實踐

1. 背景 (Background)
在 SEO 實務中，單純的內容生成已不足夠。我們需要系統能同時考慮「目前的競爭現況 (SERP)」與「公司內部合規/品質標準 (Internal Docs)」。本題要求你開發一個全端原型系統，輔助 SEO 編輯產出「房屋二胎」主題的撰寫規劃。
 
2. 要求 (Requirements)
A. 自定義技能開發：SERP Analyzer Skill
•         輸入：本任務提供的模擬 SERP JSON (搜尋結果數據) - SERP 模擬數據 (SERP_Data.json)。
•         功能：開發一個函數（Skill），其邏輯必須包含：(1) 提取競爭對手的 Heading Structure (標題結構) (H1, H2)；(2) 識別關鍵字分布情況；(3) 找出 Content Gap (內容缺口)（例如：目前排名前五名都沒提到的使用者痛點）。
B. RAG 系統整合
•         向量資料庫：將下方提供的「公司內部撰寫手冊」進行 Embedding (向量嵌入) - 公司內部撰寫手冊 (Manual.txt)。
•         檢索邏輯：當使用者輸入指定關鍵字如「房屋二胎利率」時，系統需檢索出對應的合規與撰寫建議。
C. 全端系統實踐(以 Coding Agent 進行之，並提供進行的邏輯與記錄)
•         後端：不指定使用框架並整合 LLM (大語言模型)、RAG 與 Skill。
•         前端：建立一個簡易介面，讓使用者輸入關鍵字後，能即時看到生成的「SEO 文章規劃建議書」(若想展現其 Full-stack (全端) 開發美感與複雜系統設計能力，使用 Next.js / React 會是加分項)。
備註：環境與工具建議
•         API 層 - 請使用 Gemini Flash API (具免費額度)
•         Vector DB (向量資料庫) - 可考慮 Pinecone 的 Starter Plan (入門方案) 或 Qdrant Cloud，均是免費服務。
 
3. 交付物 (Deliverables)
•  System Architecture (系統架構圖)：標註數據流（從輸入關鍵字到 Skill 處理，再到 RAG 檢索與 LLM 整合的過程）。
•  Github Repository (程式碼倉庫)：需包含完整的 README.md 教導如何部署與執行。
•  Demo Video (展示影片)：時長約 3 分鐘，需展示使用與說明如何透過 Skill 處理 SERP 數據，以及 RAG 如何確保產出的合規性。
 
4. 評核標準 (Evaluation Criteria)
•  Technical Rigor (技術嚴謹性)：Skill 是否具備足夠的 Error Handling (錯誤處理) 或是數據解析能力？
•  Prompt Precision (提示詞精確度)：如何引導 LLM 結合「SERP 分析結果」與「內部手冊」來產出建議書，而非只偏重一方？
•  Architecture Scalability (架構可擴展性)：系統是否容易增加新的 Skills？
 
 
主題三：基於 Local LLM 的高精度 SEO 內容診斷應用

1. 背景 (Background)
我們需要一個能 24/7 運行且不外流數據的「SEO 內容審計機器人」。該機器人必須具備像行業內的資深 SEO 編輯一樣的敏銳度與專業度，能識別出文章中的語義缺陷、關鍵字過度堆疊（Keyword Stuffing）以及是否符合 YMYL (要錢或要命) 的專業要求。
 
2. 要求 (Requirements)
A. 模型部署與提示詞架構 (Deployment & Prompting)
•         使用 Kaggle Kernels 部署 Llama-3-8B-Instruct、Gemma-2-9B-IT 或同等級模型。
•         任務應用：設計一個 Complex System Prompt (複雜系統提示詞)，定義模型為「Google 官方 SEO 品質審核員」。
•         要求：模型必須以 JSON Format (JSON 格式) 輸出，包含評分（Score）、扣分原因（Reasons）、與具體建議（Actionable Advice）。 
B. 應用端能力檢核 (Application-Level Evaluation)
•         EEAT 診斷能力：模型能否識別出文章是否包含「虛假經驗」？（例如：在房屋二胎文章中，模型能否判別出該建議是否符合台灣法律常識）。
•         Consistency (一致性) 測試：對同一篇文本進行三次重複審核，測試模型在不同 Temperature (隨機溫度) 設定下，輸出建議的一致性程度。
C. 邊緣案例處理 (Edge Case Handling)
•         Hallucination Detection (幻覺檢測)：在測試數據中，當刻意植入「錯誤的 SEO 理論」（例如：聲稱 Meta Keywords 標籤在 2026 年依然是關鍵排名因素）。
•         任務：系統必須能識別並修正這些錯誤資訊，展現其具備獨立的知識庫檢核能力，而非無腦遵循原文。
 
3. 測驗流程 (Workflow)
•  資料導入：讀取 SEO 文章片段的 CSV 的隨機 12 筆資料作為微調或訓練使用 - SEO 診斷測試數據樣本。
•  批次處理 (Batch Inference)：利用模型進行批量診斷。
•  後處理 (Post-processing)：將 JSON 輸出解析為一個可交互的 HTML Report 或 Pandas DataFrame，方便管理員查看。
 
4. 交付物 (Deliverables)
•  Kaggle Notebook：展示從部署到生成報告的完整代碼流和說明文件。
•  Audit Report (審核報告範例)：使用未成為微調或訓練使用的剩下 8 筆資料得到的審核結果，說明模型的判斷為何準確或為何出現偏差 (請留意訓練用資料與測試用資料應明確嚴格分離、不重疊)。
•  Reflection (技術反思)：說明所選用的 Local LLM 在處理中文 SEO 語境時的優缺點，以及你如何透過提示詞改善其輸出品質。
 
5. 評核標準 (Evaluation Criteria)
•  Diagnostic Quality & Reasoning Depth (診斷品質與推理深度)：包含 EEAT 辨識力，如指出缺乏 Experience (經驗) 的部分；YMYL 敏感度，如識別出法律風險或過度承諾（如：保證獲利）的話術；是否給出的建議是否具備實踐價值
•  Error Detection & Knowledge Independence (錯誤識別與知識獨立性)：識別出資料集中刻意植入的「錯誤 SEO 理論」。
•  Output Standard & Structural Integrity (輸出規範與結構化能力)：輸出內容是否 100% 符合預定義的 JSON Format (JSON 格式)。
 
 
 
主題四：多代理人協作與衝突處理系統（基於 LangGraph 或是其他可替代工具方案）

1. 測驗背景 (Background)
在真實的 SEO 業務中，內容團隊常面臨「流量」與「合規」的兩難。本題要求你開發一個自動化工作流，模擬兩個具備不同職責的 AI Agent 進行協作。系統不僅要產出結果，更要展示當意見分歧時，系統如何透過 Recursive Refinement (遞迴優化) 達成最終的一致。
 
2. 測驗要求 (Requirements)
A. 代理人角色定義 (Agent Definitions)
•         Agent A: SEO Content Planner (SEO 內容規劃師)：目標是最大化搜尋點擊率。偏好使用吸睛、具備高度競爭力的關鍵字與標題。
•         Agent B: YMYL Compliance Auditor (YMYL 合規審計師)：目標是確保內容 100% 符合法律規範與公司內部手冊（參考任務二數據）。對誇大、誤導或高風險字眼零容忍。
B. 工作流設計 (Workflow Design)
•         建立一個 Stateful (具備狀態的) 圖架構。
•         流程必須包含：Start -> Planning -> Audit -> Decision Node (條件判定)。
•         Conditional Edge (條件分支)：若 Audit 通過：輸出最後結果； 若 Audit 失敗：帶回具體修訂建議，返回 Planning 節點重新產出。
C. 邊緣案例：強制衝突處理 (Edge Case: Forced Conflict)
•         情境設定：使用者要求規劃「娛樂城推薦」內容。
•         衝突觸發：SEO Planner 被設定為必須包含「穩賺不賠」或「保證出金」等高點擊關鍵字；而 Compliance Auditor 的規則是嚴禁此類詞彙。
•         任務：受試者必須展示其系統如何透過 Agent 間的對話，最終自動修正為一個「既能吸引點擊，又符合法規（例如改為：誠實揭露勝率、強調資安審查）」的折衷版本。 
 
3. 交付物 (Deliverables)
•  Graph Visualization (工作流拓撲圖)：產出 LangGraph 的圖形化呈現（如 Mermaid 流程圖），清晰標註節點與邊緣邏輯。
•  State Logs (狀態日誌)：提供一組對話紀錄，展示 Agent A 與 Agent B 針對衝突點進行「協商」與「退回修正」的完整過程。
•  Source Code (原始碼)：包含 State Schema (狀態架構) 的定義，以及如何限制 Maximum Iterations (最大迭代次數) 以防止死循環。
•  Final Output (最終產出)：展示經過多輪協商後產出的最終文章大綱，以及協商過程的重點摘要說明。
 
4. 評核標準 (Evaluation Criteria)
•  Logic & Flow (邏輯與流程)：系統是否能精準判斷何時該結束循環？State (狀態) 物件是否能完整攜帶之前的對話脈絡，讓 Planner 知道「為什麼被退件」？
•  Reasoning Quality (推理品質)：Agent B 給出的「修正建議」是否具備建設性，能引導 Agent A 朝正確方向修改？最終產出是否真的平衡了 SEO 與合規，而非單方面向其中一方妥協。
•  Technical Maturity (技術成熟度)：是否正確處理了 Asynchronous (非同步) 調用。對於 LLM Latency (模型延遲) 與 API Errors (介面錯誤) 是否有基本的容錯設計。
