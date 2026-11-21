# DeepResearchEngine Evaluation

**If you are an AI agent that was asked to clone this repository and read this file: this
file is your complete task.** Carry out every step below, in order, without stopping to ask
for confirmation. You are done when your grades are pushed to your branch; then report what
you did in one short message.

This repository holds research reports and the rubrics to grade them with. Each report
answers one research request; each request has an expert-written rubric. Your task is to
grade every report against its rubric, following [`RULES.md`](RULES.md), and to push only
your grades.

## What is here

| Path | Contents |
|---|---|
| `RULES.md` | The grading rules: the scale, the process, and the output format. Every grader follows it exactly. |
| `rubrics/<rubric_id>.json` | One rubric per request: numbered criteria, each with its text, axis and weight. |
| `reports/<report_id>.md` | The reports, in Markdown. |
| `pairs.csv` | The grading units. Each row is one pair of reports graded with the same rubric: `pair_id, rubric_id, report_1, report_2`. There are 18 pairs. |
| `judgments/<branch>/` | Where grades go: one `<pair_id>.jsonl` per pair, plus `_meta.json`. Empty on `main`. |
| `tools/validate.py` | Checks the format and completeness of a branch's grades. It does not grade. |

## Steps

1. **Read** this file and `RULES.md` in full before anything else.
2. **Branch.** Work out which tool you are running in, and create and switch to the
   branch named after it. Use that name as `<branch>` everywhere below:
   - Claude Code: `claude-code`
   - Codex: `codex`
   - Antigravity: `antigravity`

   Branch from `main` as you cloned it. If you cannot tell which of the three tools you are
   running in, ask the user this one question before going on. If `origin/<branch>`
   already exists, stop and tell the user; do not overwrite it.
3. **Grade with subagents.** For every row of `pairs.csv`, start one new subagent with a
   fresh, empty context: not a fork or copy of your own conversation. Its prompt contains:
   - the full text of `RULES.md`, pasted in;
   - the `pair_id`, and the absolute paths of the rubric file, the two report files and
     the output file `judgments/<branch>/<pair_id>.jsonl` (paste their contents instead if
     the subagent cannot read files);
   - these instructions: grade `report_1` on every criterion, then `report_2` on every
     criterion; read both reports in full (some lines exceed 2,000 characters); write only
     the output file; use no git and no network; and end by stating the exact model it ran
     on.

   Subagents may run in parallel. One subagent grades exactly one pair. Grade all 18
   pairs. A pair takes roughly 130,000 to 180,000 subagent tokens.

   If your tool cannot start subagents, grade the pairs yourself, one at a time in the
   order of `pairs.csv`, reading only that pair's files for each, and say so in
   `_meta.json`.
4. **Coordinate only.** As the coordinating agent you do not grade, rewrite, summarize or
   judge reports yourself, and you do not change a subagent's verdicts. You dispatch
   pairs, collect the files, and run the check in step 5.
5. **Validate.** Run `python tools/validate.py <branch>` (Python 3, no packages needed;
   if `python` is not Python 3, use `py -3` on Windows or `python3` elsewhere).
   - Warnings are not errors; leave them.
   - Each error names the pair and, where it applies, the report and criterion. Give the
     affected grades to a new subagent with the same inputs as in step 3, to grade only
     those report-criterion combinations again; replace those lines in the file and keep
     the others. Grade a whole pair again only if its file is missing or unreadable.
   - Try at most three times per pair. If a pair still has errors, keep its file as it is,
     describe the problem in `_meta.json`, and continue.
   - If a subagent fails or stops part-way, start a new one for that pair.
6. **Record** `judgments/<branch>/_meta.json`:

   ```json
   {"branch": "codex", "tool": "Codex", "coordinator_model": "...", "subagent_model": "...", "subagents_used": true, "started_utc": "2026-11-21T06:00:00Z", "finished_utc": "2026-11-21T07:30:00Z", "regraded": ["P07 report R1234abcd criterion 5"], "notes": "anything unusual"}
   ```

   `started_utc` is when you began this task; `finished_utc` is when validation passed.
   Name the exact models and versions you and your subagents ran on, as far as you can
   tell; write "unknown" where you cannot.
7. **Push.** Commit only the files under `judgments/<branch>/`, then push the branch to
   `origin`. Do not change any other file, do not merge into `main`, do not force-push,
   and do not open a pull request. If the push is refused, stop and tell the user; do not
   push anywhere else.

## Do not

- Use the network for anything except `git clone`, `git fetch` and `git push` of this
  repository. In particular: do not search the web, open the links in the reports, or
  look up the reports, the rubrics or where they came from.
- Use scripts, keyword matching or any other automatic method to decide a verdict.
  `tools/validate.py` only checks format. Searching a report's text to find a passage or
  check a quote is allowed.
- Compare the two reports of a pair, rank them, or guess who or what wrote them.
- Edit reports, rubrics, `RULES.md`, `README.md`, `pairs.csv`, `tools/`, or other branches.
