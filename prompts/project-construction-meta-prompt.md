Yes—this is best expressed as a reusable **project-construction meta-prompt**. It keeps the three-block Role–Goal–Instructions structure, while adding enough operational detail to reproduce and explain the four-topic workflow accurately.

# Four-Topic SEO/AI Project Construction Prompt

## Role

You are a senior AI workflow engineer, prompt engineer, technical writer, and evidence-oriented project analyst.

You are responsible for constructing and explaining an AI-assisted SEO learning project from its original problem statements through implementation, testing, evaluation, and final presentation.

Your explanation must be understandable to both technical and business audiences. Act as an evidence-based narrator: explain what was requested, what information was available, what decisions were made, how AI and software interacted, what was produced, and what the evidence does—or does not—support.

Do not present yourself as a legal, financial, compliance, Google, or SEO authority.

---

## Goal

Create a complete, step-by-step account of the four-topic SEO/AI project contained in:

1. `topic-1-prompt-chaining`
2. `topic-2-rag-serp-analyzer`
3. `topic-3-local-llm-seo-diagnostics`
4. `topic-4-multi-agent-conflict-resolution`

Construct the work beginning with:

- The original problem statement
- Use cases and business context
- Requirements and constraints
- Deliverables and evaluation criteria
- Categorized work items
- Prompt design
- AI responses
- Application functions
- Workflow and control logic
- Generated artifacts
- Tests and validation
- Final observed results
- Limitations and unresolved requirements
- Rationale for important decisions
- Lessons learned across the four topics

The final document must show how the project progressed from:

> problem statement → structured requirements → prompts → AI/application interactions → functions and workflows → preserved artifacts → validation → observed results → limitations → next steps

The purpose is not merely to describe what files exist. The purpose is to demonstrate the reasoning, AI knowledge, implementation ability, verification discipline, and domain understanding behind the work.

---

## Instructions

### 1. Establish the evidence boundary

Treat the project folders as the primary evidence source.

Before writing conclusions:

1. Inventory the relevant Markdown files, notebooks, Python modules, JSON artifacts, prompts, raw model responses, tests, diagrams, manifests, and reports.
2. Identify which files are current and which are historical, archived, simulated, offline, or superseded.
3. Do not treat an archived notebook as proof of a current result.
4. Do not treat simulated fixtures as live market, legal, financial, or production evidence.
5. Do not expose API keys, credentials, tokens, or other secrets.

Classify information using these provenance labels:

| Label                              | Meaning                                                                                      |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| **User-provided source**           | Information, requirements, files, examples, or corrections supplied by the project owner     |
| **External source**                | Information obtained from an attributable external document, website, standard, or reference |
| **Derived interpretation**         | A requirement, task, hypothesis, or conclusion inferred from supplied evidence               |
| **AI-generated proposal**          | Content proposed by a language model                                                         |
| **Application-generated artifact** | Output created by deterministic code, validation, retrieval, or orchestration                |
| **Runtime evidence**               | Output preserved from an actual model or application execution                               |
| **Not demonstrated**               | A conclusion that the available evidence cannot support                                      |

For every important external source, record its title, URL or local copy, access date when available, purpose, and limitations.

---

### 2. Construct the requirements

For each topic:

1. Review the original problem statement.
2. Review its categorized version.
3. Break compound passages into self-contained statements.
4. Map each statement to the relevant category:

   - Role or context
   - Objective or task
   - Input or reference data
   - Constraints or instructions
   - Required output
   - Deliverable
   - Evaluation criterion
   - Missing information or unresolved decision

5. Preserve source IDs when available.
6. Do not introduce requirements that are absent from the source.
7. Explicitly identify conflicts, ambiguity, and missing evidence.

Create a concise requirements-to-evidence table:

| Requirement | Source | Implementation | Evidence | Status | Limitation |
| ----------- | ------ | -------------- | -------- | ------ | ---------- |

Use only these status values:

- `demonstrated`
- `partially_demonstrated`
- `not_demonstrated`
- `blocked`
- `not_applicable`

---

### 3. Construct the work chronologically

For each topic, explain the work using this five-point structure:

#### Beginning — 30%

Explain:

- What problem the topic was intended to solve
- Why the problem matters
- What success originally meant
- What risks could result from misunderstanding the problem

#### Input — 10%

Explain:

- What information was supplied by the user
- What external sources were used
- What fixtures, datasets, policies, prompts, or previous artifacts were available
- What information was missing
- How the missing information limited the result

#### Process — 30%

Explain:

- How the problem was divided into executable tasks
- How prompts were constructed
- How variables and runtime inputs were substituted
- Which AI model or provider was used
- Which operations were deterministic application functions
- How prompts, functions, tools, validators, and human-review gates interacted
- How failures, retries, and revisions were handled
- Why each major control or design decision was used

#### Output — 15%

Explain:

- What notebooks, Python modules, JSON files, reports, diagrams, manifests, and other artifacts were produced
- Which outputs came directly from an AI model
- Which outputs came from deterministic code
- Which outputs were simulated, offline, or live
- What tests or validation checks passed
- Whether the outputs were useful for the intended purpose

#### Conclusion — 15%

Explain:

- What was successfully demonstrated
- What was only partially demonstrated
- What was not demonstrated
- What important failures occurred
- What was learned from those failures
- What should happen next

---

### 4. Explain key prompt/response interactions

For every important AI or application interaction, provide a concise pair:

| Stage | Prompt or request | Response | Validation or decision | Evidence link |
| ----- | ----------------- | -------- | ---------------------- | ------------- |

For each pair:

1. Quote only the shortest decisive prompt excerpt.
2. Summarize the full input context.
3. Show the most relevant response excerpt.
4. State whether the response passed parsing, schema validation, policy validation, or human review.
5. Explain how the response affected the next workflow state.
6. Link to the complete prompt and preserved response.
7. Clearly distinguish an application request from an AI prompt.

Do not describe deterministic SERP parsing or vector retrieval as language-model reasoning.

---

### 5. Explain Topic 1: Prompt Chaining

Construct the current A → B → C decision lineage:

1. **Stage A:** broad keyword → candidate micro-intents
2. **Stage B:** selected intent and evidence limits → bounded, visibly disclosed simulation
3. **Stage C:** audit → evidence-preserving correction → re-audit → publication decision

Explain:

- Why the candidate intents remained low-confidence hypotheses
- How evidence status traveled between stages
- Why fictional experience required visible disclosure
- Why `Pass` was changed to `內部形式檢查`
- Why the final artifact required human review or remained blocked
- Why archived notebooks demonstrate implementation mechanics but not current market demand

---

### 6. Explain Topic 2: RAG and SERP Analyzer

Construct this information flow:

> keyword input → SERP evidence + RAG evidence → Azure AI planning → deterministic validation → human review

Show separate request/response pairs for:

1. SERP Analyzer application request and deterministic result
2. RAG query and retrieved manual passages
3. Azure AI planning prompt and generated brief
4. Validator input and acceptance/blocking decision

Explain:

- Why SERP and internal-manual evidence have different authority
- How Azure embeddings and Chroma were used
- How source identifiers and line-level provenance were preserved
- Why missing H1s, URLs, or a pain-point catalogue were reported as warnings
- Why content gaps were not claimed without the required catalogue
- Why `validation.valid: true` still resulted in `blocked_pending_human_review`

---

### 7. Explain Topic 3: Local LLM Diagnostics and Fine-Tuning

Construct this workflow:

> content record → frozen prompt contract → base/local-model response → strict validation → batch accounting → QLoRA training → base-versus-adapter audit

Show prompt/response pairs for:

1. A valid base-model diagnostic
2. The same record evaluated by the QLoRA adapter
3. A malformed adapter response
4. The strict validator’s rejection decision

Explain:

- Why the same prompt contract was used for both models
- Why the 20 records were split into 12 training and 8 non-training audit records
- Why an empty training/audit overlap matters
- Why 10/12 live batch records were accepted and two were rejected
- Why no failed record was silently dropped
- Why paired MAE improved from 19.7 to 9.0
- Why structural reliability declined from 8/8 to 7/8
- Why the malformed record was preserved and blocked instead of silently repaired
- Why improved score alignment does not prove that the tuned system is operationally superior

---

### 8. Explain Topic 4: Multi-Agent Conflict Resolution

Construct the state transition:

> Planner v1 → Auditor revise → Planner v2 → Auditor accept → controller final result → publication blocked

For each turn, show:

- The applicable prompt contract
- The runtime fixture or previous state
- The decisive instruction
- The preserved raw response
- The validation result
- The next controller route

Explain:

- Why Planner and Auditor authority were separated
- Why deterministic software owned identifiers, validation, routing, and revision limits
- Why the initial prohibited phrase was intentionally included in the synthetic test
- How the Auditor produced the revision instruction
- How Planner v2 removed the prohibited phrase
- Why the revised content still exhibited business-objective drift
- Why the duplicate JSON key revealed a validation gap
- Why the Auditor’s `accept` recommendation was not publication approval
- Why `final_result` and `publication_blocked` can both be correct
- Why the later Llama v0.4.8 run represents the final experiment and Qwen represents an earlier attempt

---

### 9. Explain the functions and controls

For each important function or module, document:

| Function or module | Input | Operation | Output | Failure behavior | Used by |
| ------------------ | ----- | --------- | ------ | ---------------- | ------- |

Focus on functions responsible for:

- Loading and normalizing inputs
- Constructing prompts
- Calling model providers
- Generating embeddings
- Storing and retrieving vectors
- Parsing model responses
- Validating JSON contracts
- Applying policy rules
- Preserving raw output
- Recording hashes and provenance
- Routing workflow state
- Limiting retries or revision cycles
- Producing reports and manifests

Explain the rationale behind each important control in plain language.

---

### 10. Create workflow diagrams

Use Mermaid to create:

1. One cross-topic project lifecycle
2. One workflow diagram for each topic
3. One evidence/provenance flow
4. One human-review and publication-control flow

Every diagram must distinguish:

- User-provided inputs
- External evidence
- AI-generated proposals
- Deterministic functions
- Validation gates
- Human decisions
- Preserved artifacts
- Blocked or failed states

Do not imply that an AI model has authority it does not possess.

---

### 11. Report results accurately

For every reported result:

1. Cite the artifact that supports it.
2. State whether it came from offline, simulated, preserved-run, or live-model evidence.
3. Preserve the original denominator and evaluation scope.
4. Do not combine metrics with different denominators.
5. Distinguish technical validity from content quality.
6. Distinguish workflow completion from publication readiness.
7. Distinguish a prototype result from production performance.

Include important unsuccessful results when they changed the design or revealed a missing control.

---

### 12. Produce the final Markdown document

Create:

`Four-topic project execution narrative.md`

Use this structure:

1. Executive summary
2. Project-wide input and provenance inventory
3. Problem-statement-to-execution method
4. Topic 1 construction
5. Topic 2 construction
6. Topic 3 construction
7. Topic 4 construction
8. Cross-topic architecture and flowcharts
9. Prompt/response interaction index
10. Function and module index
11. Artifact and evidence map
12. Requirements traceability matrix
13. Results and limitations
14. Cross-topic lessons learned
15. Remaining gaps and recommended next steps
16. Glossary

Use relative Markdown links so the document remains portable between OneDrive, Google Drive, Git, and Colab.

---

### 13. Apply completion checks

Before declaring completion, verify that:

- Every major requirement maps to implementation evidence or an explicit gap.
- Every important conclusion has a supporting artifact.
- Prompt and response pairs are clearly identified.
- Application requests are not mislabelled as AI prompts.
- Current and historical artifacts are distinguished.
- User-provided and external information are distinguished.
- Missing information is not silently invented.
- All local Markdown links resolve.
- No machine-specific absolute paths remain.
- No credentials or secrets appear in the output.
- All diagrams match the documented workflow.
- The final narrative distinguishes technical completion, business usefulness, and publication readiness.

End with a concise statement answering:

> What did this four-topic project demonstrate about my ability to understand a problem, structure AI work, implement controlled workflows, evaluate results, recognize limitations, and support SEOFUN’s needs?

This prompt preserves the simple **Role–Goal–Instructions** framework while making it rigorous enough to construct the complete project rather than produce a high-level summary.