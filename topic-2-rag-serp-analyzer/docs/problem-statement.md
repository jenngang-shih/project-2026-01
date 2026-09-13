<!--
Traceability:
  Source file: docs/problem-statement.md (project root, original combined document)
  Topic: 2 — 主題二：全端 RAG 系統與 Custom Skill (自定義技能) 實踐
  Extraction method: split on delimiter pattern `主題*：` (regex: ^主題[一二三四]：)
  Extracted: verbatim, no edits to original content below this header
-->

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
