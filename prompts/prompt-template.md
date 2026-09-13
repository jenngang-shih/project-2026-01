# prompt-template

A schema for both (a) authoring new prompts and (b) categorizing raw requirements
(e.g. from `problem-statement.md`) into structured, reusable prompt components.

## Role (Context)
Definition: Who the AI should act as — domain expertise, perspective, or persona
implied by the task.
Example: You are an expert {Insert Profession/Role}.

## Objective (Task)
Definition: The core action(s) the AI must perform — what to produce or
accomplish. Answers "what is the task," not "how" or "what to hand in."
Example: Your goal is to {Insert Clear Action item like create, analyze, or summarize}.

## Constraints (Instructions)
Definition: Rules governing *how* the task is performed — format, tone, scope
limits, target audience, required tools/frameworks/APIs, technical limits.
Distinguish from Objective (what to do) and from Deliverables (what to hand in).
Example: Format this as a {bullet points/table/essay}. Use a {tone} tone tailored
for {Target Audience}. Must use {specific API/framework} if specified.

## Reference (Data/Context)
Definition: Background data, existing materials, or source content the AI should
draw on, retrieve from, or stay consistent with (e.g. provided datasets, manuals,
prior outputs from earlier stages in a chain).
Example: Use the following background data and specific examples to guide your
response: {Insert data or text}.

## Deliverables
Definition: The concrete artifact(s) that must exist at the end of the task, in
what form. Distinct from Objective (the task's purpose) and from Evaluation
Criteria (how those artifacts are judged) — this category answers only
"what must be produced/submitted."
Example: Produce {Insert artifact list, e.g. an architecture diagram in Mermaid,
a README.md, a 3-minute demo video}.

## Evaluation Criteria
Definition: The dimensions along which the deliverables' *quality* will be
judged — not what to produce, but how well it must perform against stated
standards.
Example: This is successful if {Insert measurable/qualitative criteria, e.g.
logical consistency between stages, absence of hallucinated claims, 100%
adherence to a specified output format}.

---

## Notes on category boundaries (for categorization use)

- **Objective vs. Constraints**: Objective = the verb/action; Constraints = the
  rules around performing it (format, tone, required tools, limits).
- **Constraints vs. Deliverables**: Constraints govern the process; Deliverables
  govern the end artifact(s) to be submitted.
- **Deliverables vs. Evaluation Criteria**: Deliverables = what exists at the
  end; Evaluation Criteria = how good it needs to be / what it's judged against.
- If a bullet doesn't cleanly fit one category, assign it to the closest fit
  and flag it with `[needs review]` rather than forcing an exact match.
