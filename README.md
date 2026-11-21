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
| `pairs.csv` | The grading units. Each row is one pair of reports graded with the same rubric: `pair_id, rubric_id, report_1, report_2`. |
| `judgments/<branch>/` | Where grades go: one `<pair_id>.jsonl` per pair, plus `_meta.json`. Empty on `main`. |
| `tools/validate.py` | Checks the format and completeness of a branch's grades. It does not grade. |

## Steps

1. **Branch.** Work out which tool you are running in, and create and switch to the
   branch named after it. Use that name as `<branch>` everywhere below:
   - Claude Code: `claude-code`
   - Codex: `codex`
   - Antigravity: `antigravity`

   Branch from `main` as you cloned it. If you cannot tell which of the three tools you are
   running in, ask the user this one question before going on.
2. **Read** `RULES.md` in full before anything else.
3. **Grade with subagents.** For every row of `pairs.csv`, start one subagent with a
   fresh context. Give it the full text of `RULES.md`, the rubric file of the row, the two
   report files of the row, the `pair_id`, and the output path
   `judgments/<branch>/<pair_id>.jsonl`. The subagent grades `report_1` on every
   criterion, then `report_2` on every criterion, and writes the file. Subagents may run
   in parallel. One subagent grades exactly one pair. Grade all 18 pairs.
4. **Coordinate only.** As the coordinating agent you do not grade, rewrite, summarize or
   judge reports yourself, and you do not change a subagent's verdicts. You dispatch
   pairs, collect files, and check them.
5. **Validate.** Run `python tools/validate.py <branch>` (Python 3, no packages needed;
   use `python3` if `python` is not Python 3). If it reports a problem in a pair, give
   that pair to a new subagent to grade again in full, replacing the file. Repeat until
   the check reports no errors.
6. **Record** `judgments/<branch>/_meta.json`:

   ```json
   {"branch": "codex", "tool": "Codex", "coordinator_model": "...", "subagent_model": "...", "started_utc": "2026-11-21T06:00:00Z", "finished_utc": "2026-11-21T07:30:00Z", "notes": "anything unusual, such as a pair graded twice"}
   ```

   Name the exact models and versions you and your subagents ran on, as far as you can
   tell.
7. **Push.** Commit only the files under `judgments/<branch>/`, then push the branch to
   `origin`. Do not change any other file, do not merge into `main`, and do not open a
   pull request. If the push is refused for lack of permission, stop and tell the user;
   do not push anywhere else.

## Do not

- Use the network for anything except `git clone`, `git fetch` and `git push` of this
  repository. In particular: do not search the web, open the links in the reports, or
  look up the reports, the rubrics or where they came from.
- Use scripts, keyword matching or any other automatic method to decide a verdict.
  `tools/validate.py` only checks format.
- Compare the two reports of a pair, rank them, or guess who or what wrote them.
- Edit reports, rubrics, `RULES.md`, `README.md`, `pairs.csv`, `tools/`, or other branches.
