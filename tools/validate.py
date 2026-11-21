"""Check the format and completeness of one branch's grades. It does not grade.

Usage: python tools/validate.py <branch>

Checks every pair in pairs.csv: the file exists; every line is a JSON object with exactly
the fields of RULES.md; every combination of the pair's two reports and the rubric's
criteria appears once; verdict and score agree; confidence is in [0, 1]; and every
evidence quote occurs in the report (ignoring case, whitespace, Markdown emphasis and
quote styles; "..." splits a quote into parts that must each occur; a link may be quoted
by its text or its URL). Errors name the pair, line, report and criterion, so only the
affected grades need redoing. Missing quotes on a verdict that needs one, and missing
elements listed on a Satisfied verdict, are warnings. Exit status 1 when any error is found.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIELDS = {"pair_id", "report_id", "criterion_index", "verdict", "score", "confidence",
          "reasoning", "evidence_quotes", "missing_elements"}
SCORES = {"Satisfied": 1.0, "Partially Satisfied": 0.5, "Not Satisfied": 0.0}
QUOTE_CHARS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"',
                             "–": "-", "—": "-", " ": " "})


def norm(text: str, links: str = "text") -> str:
    """Normalize for quote matching. links="text" keeps a Markdown link's text only;
    links="both" keeps its text and its URL, so a quoted URL also matches."""
    text = text.translate(QUOTE_CHARS)
    text = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", r"\1 \2" if links == "both" else r"\1", text)
    text = re.sub(r"[*_`#>]", "", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def quote_found(quote: str, report_variants: tuple[str, ...]) -> bool:
    for mode in ("text", "both"):
        parts = [norm(p, mode) for p in re.split(r"\.\.\.|…|\[\.\.\.\]", quote)]
        parts = [p.strip(" .,;:") for p in parts]
        parts = [p for p in parts if len(p) >= 4]
        if not parts:
            return True
        if any(all(p in variant for p in parts) for variant in report_variants):
            return True
    return False


def main() -> int:
    # Quotes contain characters such as ε or ≥; a Windows console (cp1252) would crash on them.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    branch = sys.argv[1]
    out_dir = ROOT / "judgments" / branch
    errors: list[str] = []
    warnings: list[str] = []

    with open(ROOT / "pairs.csv", encoding="utf-8", newline="") as f:
        pairs = list(csv.DictReader(f))
    rubrics = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "rubrics").glob("*.json")}
    reports = {}
    for p in (ROOT / "reports").glob("*.md"):
        raw = p.read_text(encoding="utf-8")
        reports[p.stem] = (norm(raw, "text"), norm(raw, "both"))

    if not (out_dir / "_meta.json").is_file():
        warnings.append(f"{out_dir.relative_to(ROOT)}/_meta.json is missing (write it before pushing)")

    complete = 0
    for pair in pairs:
        pid, rid = pair["pair_id"], pair["rubric_id"]
        members = [pair["report_1"], pair["report_2"]]
        criteria = {c["index"]: c for c in rubrics[rid]["criteria"]}
        path = out_dir / f"{pid}.jsonl"
        if not path.is_file():
            errors.append(f"{pid}: {path.relative_to(ROOT)} is missing")
            continue
        seen: dict[tuple[str, int], int] = {}
        pair_errors = 0
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            where = f"{pid} line {n}"

            def bad(msg: str) -> None:
                nonlocal pair_errors
                pair_errors += 1
                errors.append(f"{where}: {msg}")

            try:
                row = json.loads(line)
            except json.JSONDecodeError as e:
                bad(f"not JSON ({e.msg})")
                continue
            if not isinstance(row, dict) or set(row) != FIELDS:
                got = set(row) if isinstance(row, dict) else set()
                bad(f"fields must be exactly {sorted(FIELDS)}; missing {sorted(FIELDS - got)}, extra {sorted(got - FIELDS)}")
                continue
            if row["pair_id"] != pid:
                bad(f"pair_id {row['pair_id']!r} should be {pid!r}")
            if row["report_id"] not in members:
                bad(f"report_id {row['report_id']!r} is not in this pair")
                continue
            idx = row["criterion_index"]
            if not isinstance(idx, int) or idx not in criteria:
                bad(f"criterion_index {idx!r} is not in rubric {rid}")
                continue
            key = (row["report_id"], idx)
            if key in seen:
                bad(f"duplicate of line {seen[key]} ({row['report_id']}, criterion {idx})")
            seen[key] = n
            verdict, score = row["verdict"], row["score"]
            if verdict not in SCORES:
                bad(f"verdict {verdict!r} must be one of {list(SCORES)}")
            elif not isinstance(score, (int, float)) or float(score) != SCORES[verdict]:
                bad(f"score {score!r} does not match verdict {verdict!r} ({SCORES[verdict]})")
            conf = row["confidence"]
            if not isinstance(conf, (int, float)) or not 0 <= conf <= 1:
                bad(f"confidence {conf!r} must be a number from 0 to 1")
            if not isinstance(row["reasoning"], str) or not row["reasoning"].strip():
                bad("reasoning must be a non-empty string")
            for name in ("evidence_quotes", "missing_elements"):
                if not isinstance(row[name], list) or not all(isinstance(x, str) for x in row[name]):
                    bad(f"{name} must be a list of strings")
            if isinstance(row["evidence_quotes"], list):
                for q in row["evidence_quotes"]:
                    if isinstance(q, str) and not quote_found(q, reports[row["report_id"]]):
                        bad(f"report {row['report_id']} criterion {idx}: evidence quote not found: {q[:80]!r}")
                if verdict in SCORES and verdict != "Not Satisfied" and not row["evidence_quotes"]:
                    warnings.append(f"{where}: {verdict} on criterion {idx} without an evidence quote")
            if verdict == "Satisfied" and isinstance(row["missing_elements"], list) and row["missing_elements"]:
                warnings.append(f"{where}: Satisfied on criterion {idx} but missing_elements is not empty")
        expected = {(r, i) for r in members for i in criteria}
        missing = sorted(expected - set(seen))
        if missing:
            pair_errors += 1
            listed = ", ".join(f"report {r} criterion {i}" for r, i in missing[:10])
            errors.append(f"{pid}: {len(missing)} grade(s) missing: {listed}{' ...' if len(missing) > 10 else ''}")
        if pair_errors == 0:
            complete += 1

    for w in warnings:
        print("WARNING", w)
    for e in errors:
        print("ERROR", e)
    print(f"{complete} of {len(pairs)} pairs complete and valid; {len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
