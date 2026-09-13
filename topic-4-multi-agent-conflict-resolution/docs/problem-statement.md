<!--
Traceability:
  Source file: docs/problem-statement.md (project root, original combined document)
  Topic: 4 — 主題四：多代理人協作與衝突處理系統（基於 LangGraph 或是其他可替代工具方案）
  Extraction method: split on delimiter pattern `主題*：` (regex: ^主題[一二三四]：)
  Extracted: verbatim, no edits to original content below this header
-->

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
