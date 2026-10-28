---
name: maintainer-review-style
description: The maintainer reviews PRs lightly and hands bulk judgement work to GitHub Copilot; never report Copilot's or Claude's work as the human's
metadata:
  type: user
---

The maintainer (Yusup) said on 2026-10-16: they merge when the checks pass and a quick read finds no big problem, without reading every line; for mass questions (e.g. a 29-entry rating sheet) they use GitHub Copilot on the repository and paste its answers. They will answer questions one at a time only when each comes with plain-language context (PR numbers, jargon explained).

**Why:** the paper nearly reported a Copilot rating as a human one; the paste looked human-authored until checked.
**How to apply:** when pasted answers look machine-written, ask who produced them before recording; describe human oversight in the paper as light, not as line-by-line review. Related: [[paper-progress]].
