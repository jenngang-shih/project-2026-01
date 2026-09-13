<!--
Traceability:
  Source file: docs/problem-statement.md (project root, original combined document)
  Topic: 3 — 主題三：基於 Local LLM 的高精度 SEO 內容診斷應用
  Extraction method: split on delimiter pattern `主題*：` (regex: ^主題[一二三四]：)
  Extracted: verbatim, no edits to original content below this header
-->

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
