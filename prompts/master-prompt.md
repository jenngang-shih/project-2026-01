# categorize-topic-requirement

Role: You are an expert in requirements analysis and prompt engineering, 
structuring raw requirements into reusable LLM prompt components.


Inputs:
- `topic-{#}-*/docs/problem-statement.md` — topic-specific problem description, 
  use cases, requirements, deliverables, and evaluation criteria
- `prompts/prompt-template.md` — defines the target categories: 
  Role (Context), Objective (Task), Constraints (Instructions), Reference (Data/Context), Deliverables, and Evaluation Criteria

Instructions:
1. Load problem statement from `topic-{#}-*/docs/problem-statement.md`.
2. Break that section's text into self-contained bullet points or sentences, 
   each tagged with a short ID (e.g. B1, B2, ...) for traceability.
3. Map each tagged bullet to the prompt-template.md category it best fits 
   (Role, Objective, Constraints, Reference, Deliverables, or Evaluation Criteria). 
   If a bullet doesn't cleanly fit one category, assign it to the closest fit and 
   add a `[needs review]` note.
4. Before writing output, briefly state whether this categorization was feasible 
   given the inputs (e.g. any missing/ambiguous content) — proceed automatically 
   unless something is genuinely blocking.
5. Save the result as `problem-statement-categorized.md` in `topic-{#}-*/docs/`, preserving each item's bullet ID next to its assigned category for traceability back to the source.

# build-topic-executables

Role: You are a senior AI systems engineer who turns categorized requirements
into buildable specs — deciding, for each piece of required behavior, whether
it belongs in deterministic code or in an LLM/agent call, then writing that
piece up in the form its builder will actually need.

Inputs:
- `topic-{#}-*/docs/problem-statement-categorized.md` — the topic's requirements,
  already split into ID-tagged bullets and mapped to Role / Objective /
  Constraints / Reference / Deliverables / Evaluation Criteria
- `prompts/prompt-template.md` — Role/Objective/Constraints/Reference/
  Deliverables/Evaluation Criteria definitions, used here in compressed form
  (see step 3)

Instructions:
1. Load the categorized doc for the topic. Walk the Objective table (including
   any parent/sub-objective relationships noted there, e.g. one umbrella
   Objective realized by several stage-level sub-objectives).
2. For each Objective bullet (or tightly-linked group of sub-objectives),
   classify it as one of:
   - `deterministic` — pure code: parsing, validation, routing, data loading,
     rendering, orchestration/glue between other components.
   - `dynamic` — an LLM/agent/RAG call: anything requiring language
     understanding, generation, or judgment.
   - `hybrid` — a deterministic wrapper around one or more dynamic calls
     (the most common case — e.g. a batch loop calling an LLM per item, or a
     graph node that calls an agent then validates its output).
   State a one-sentence justification for each classification; flag genuinely
   ambiguous cases `[needs review]` rather than forcing a category.
3. For each `dynamic` component (or the dynamic part of a `hybrid` one), draft
   a compressed 3-block prompt:
   - **Role** — from the topic's categorized Role bullets, if any exist; if the
     topic has none (as categorization may reveal), say so explicitly rather
     than inventing a persona.
   - **Goal** — the driving Objective bullet(s).
   - **Instructions** — fold in everything else, labeled by source so
     traceability isn't lost:
     - *Constraints* — rules on format, tone, scope, required tools.
     - *Reference* — grounding data, prior-stage output, or fixed test
       fixtures the component must use or respect.
     - *Output shape* — derived from the relevant Deliverables bullet(s).
     - *Self-check before finalizing* — derived from the relevant Evaluation
       Criteria bullet(s), phrased as verification steps rather than grading
       rubric language.
4. For each `deterministic` component (or the wrapper part of a `hybrid` one),
   draft a function-level spec: name, inputs, outputs/return schema, required
   logic steps (from Constraints), error-handling requirements (often itself
   an Evaluation Criterion — don't drop it just because it wasn't phrased as
   a rule).
5. Add a short per-topic orchestration note: execution order across all
   components, and what output from one feeds as input/reference into the
   next (dynamic → deterministic → dynamic, etc.).
6. Before writing output, state whether building the specs was feasible given
   the categorized doc (e.g. any Objective with no clear component shape) —
   proceed automatically unless something is genuinely blocking.
7. Save output, preserving bullet IDs for traceability back to the categorized
   doc and ultimately the source problem statement:
   - Each dynamic prompt as its own file: `topic-{#}-*/prompts/<component-name>.md`
   - All deterministic specs plus the orchestration note together in:
     `topic-{#}-*/docs/component-specs.md`
