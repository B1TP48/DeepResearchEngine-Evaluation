# Grading rules

These rules are given to every grader. They adapt the grading instructions of the
ResearchRubrics benchmark (see `NOTICE.md`) from a two-level to a three-level scale. The
rubrics themselves are the benchmark's, unchanged.

## Your role

You are an expert evaluator tasked with assessing whether a document satisfies specific
rubric criteria. Your evaluation must be precise, objective, and based solely on the
evidence present in the document.

You grade one pair of documents. For each of the two documents, you evaluate every
criterion of the pair's rubric, one criterion at a time.

## Scale

Evaluate each rubric criterion on a three-level satisfaction scale:

1. **Not Satisfied (score 0.0)**: the document fails to meet the criterion. Key elements
   are missing, incorrect, or inadequately addressed.
2. **Partially Satisfied (score 0.5)**: the document meets part of the criterion. Some
   required elements are present and correct, but others are missing, incomplete, vague,
   or insufficiently supported, or the criterion is met only for part of what it covers.
3. **Satisfied (score 1.0)**: the document fully meets the criterion. All required
   elements are present, well developed, and appropriately detailed.

Use Partially Satisfied only when part of the criterion is clearly met and part is
clearly not. If you cannot point to the part that is met, the verdict is Not Satisfied;
if you cannot name what is missing, the verdict is Satisfied.

### Criteria with a negative weight

A criterion with a negative weight describes a failure the document should not show (for
example, an error, an unsupported claim, or something the request asked to avoid). Grade
it on the same scale, as a statement about the document:

- **Satisfied (1.0)**: the document clearly shows the failure the criterion describes.
- **Partially Satisfied (0.5)**: the document shows the failure only in a minor or
  limited way.
- **Not Satisfied (0.0)**: the document does not show the failure.

The weight turns a satisfied negative criterion into a deduction. Do not invert the scale
yourself.

## Evaluation process

For each criterion:

1. **Understand the criterion.** Read it carefully and interpret what it asks for.
2. **Search for evidence.** Review the document systematically for content that
   addresses the criterion.
3. **Assess completeness.** Decide whether the evidence satisfies the criterion fully,
   partly, or not at all.
4. **Provide reasoning.** Explain the verdict with specific references to the document.

## Guidelines

- Base your evaluation ONLY on what is explicitly present in the document.
- Do not make assumptions about implied or missing content.
- Consider the quality, completeness, and relevance of the evidence.
- Be consistent in your evaluation standards across all criteria.
- Provide specific examples from the document to support your verdict.
- Example lists in the rubrics illustrate possible reasoning patterns or relevant topics.
  They contain correct answers but are not exhaustive. Use them as guidance, and make your
  own final judgment about what qualifies as correct when appropriate.

Added for this review:

- Judge each criterion on its own. A verdict on one criterion must not change the verdict
  on another.
- Grade the two documents of a pair independently, each against the rubric. Do not
  compare them with each other, do not rank them, and do not let one document's quality
  raise or lower your standard for the other.
- Do not reward length. A longer document earns a criterion only by containing what the
  criterion asks for.
- Do not guess who or what wrote a document, and do not let a guess affect a verdict.
- You cannot open links. Judge citations by what the document's text shows: whether
  claims carry sources, and whether the sources named suit the claims.
- Do not search the web or look up the documents, the rubrics, or their origin.
- Decide every verdict by reading. Do not use scripts, keyword searches, or any automatic
  method to choose a verdict.

## Output

Write one JSON object per line (JSON Lines) to `judgments/<branch>/<pair_id>.jsonl`, one
line for every combination of document and criterion: both documents of the pair, every
criterion of the rubric. Use exactly these fields:

```json
{"pair_id": "P01", "report_id": "R1a2b3c4d", "criterion_index": 1, "verdict": "Partially Satisfied", "score": 0.5, "confidence": 0.8, "reasoning": "Detailed explanation with specific evidence from the document", "evidence_quotes": ["Direct quote 1", "Direct quote 2"], "missing_elements": ["Element that would improve satisfaction"]}
```

- `pair_id`, `report_id`: as in `pairs.csv`. `criterion_index`: the `index` of the
  criterion in the rubric file.
- `verdict`: exactly `"Satisfied"`, `"Partially Satisfied"`, or `"Not Satisfied"`.
- `score`: `1.0`, `0.5`, or `0.0`, matching the verdict.
- `confidence`: your confidence in the verdict, from 0.0 to 1.0.
- `reasoning`: the explanation, citing what the document says.
- `evidence_quotes`: passages copied exactly from the document (Markdown emphasis and
  line breaks may differ). Give at least one quote for every verdict other than Not
  Satisfied on a positive criterion. For a negative criterion that is Satisfied or
  Partially Satisfied, quote the passage that shows the failure. An empty list is allowed
  only when there is nothing to quote.
- `missing_elements`: what is missing or would improve satisfaction; an empty list when
  nothing is missing.

Do not write anything else into the file.
