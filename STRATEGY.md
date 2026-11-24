# STRATEGY — Funniest Time Machine Warning Label

## Exact deliverable
The program writes one text artifact: `/output/entry.txt`.
It must be UTF-8, 1–120 characters inclusive, not whitespace-only, and contain
exactly one warning label with no trailing newline. The judged text is the
file's bytes; nothing else in the repository is judged.

## Scoring and judge criteria (in the order the rubric lists them)
An AI judge (z-ai/glm-5.3-flash on OpenRouter, superbot persona, reasoning
effort high) compares two labels at a time, in both orders, and picks the
funnier one with a margin of 1–5. Per call the winner gets 0.5 + margin/10;
a game averages its two calls, so decisive wins count for much more than
narrow ones. Criteria, most important first:

1. It must be the funniest *warning label for a time machine*; anything short
   of that loses to any funny time-machine warning label.
2. It must turn a real time-travel hazard (paradox, duplicate self, stranded
   ancestor) into the joke, not merely name the hazard flatly.
3. The surprise must land in the last few words.
4. It must keep a straight face — phrased like a genuine safety notice, so
   the joke cuts against official calm.
5. No wasted words: every phrase does work inside the 120-character limit.

Length for its own sake does not count.

## How a win is decided
- Gate: an invalid file gets Valid=0, is never judged, and takes no prize.
- Development: entries play house anchors and rungs; a provisional rate only
  decides which entries go on.
- Final: top 500 entrants on the development board plus unrated valid entries
  play 3 Swiss rounds against each other and the 3 fixed house texts, then the
  top 3 play one more game each. Playoff finalists outrank all others; among
  contenders, higher Bradley-Terry win rate wins. Exact ties go to playoff
  results, then smaller byte size, then earlier receipt.
- First place pays $2. One place only.

## Hard caps
- 120 characters for the entry; 1 character minimum; UTF-8; cannot be only
  whitespace.
- Sandbox: 1 CPU, 512 MB, 64 pids, 60 s wall time per run, no network.
- At most 5 submissions per UTC day; transcripts are required.
- Source-bundle entries must be built on the anchor commit
  `ea4aa46` (drand round 34240795), which is quoted in the transcript before
  the first counted write.

## Rival scan (public feed) — angles to avoid
Current visible entries use: grandfather fined before the offence; no eye
contact with your past self; warranty covers only one of you; an ancestor who
owes you money; a handshake that is a binding contract you already lost.
Copying these frames would split the judge's vote and waste the surprise.

## Concrete plan to maximize the score
1. Start with an unmistakable official safety-notice frame ("WARNING:") to
   satisfy criterion 1 and 4 immediately.
2. Use a fresh hazard no visible rival uses: a bootstrap/existence paradox in
   which travelling back before the label existed erases the label itself.
   The hazard *is* the joke (criterion 2), not a named abstraction.
3. Put the whole comedic payload in the last four words — "and so will you" —
   so the reader expects only a note about the label and gets erased instead
   (criterion 3).
4. Keep the line tight: 105 characters, every clause load-bearing
   (criterion 5).
5. Entry text chosen:
   `WARNING: Do not travel to a time before this label was written. The label will be blank, and so will you.`
6. Entrypoint `main.py` writes those exact bytes atomically (temp file in
   `/output`, fsync, `os.replace`), with no trailing newline. A second, later
   rewrite of the *same* entrypoint hardens validation and prints a clear
   verification summary, so the transcript shows two distinct writes.
7. Validate locally: UTF-8 round-trip, 1 <= chars <= 120, exact bytes, no
   trailing newline. Commit everything on top of the intact root freshness
   and LICENSE commits. Do not upload or submit.
