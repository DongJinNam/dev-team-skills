# Report conclusions and three-sentence summaries

Apply when writing or summarizing a report that analyzes a situation and reaches a conclusion (verification, comparison, decisions or completion). Both the opening summary and any separately delivered final summary must contain **exactly three complete sentences: What → How → Why**. Evidence tables and the body have no sentence limit. Do not impose this format on ordinary conversation, simple progress updates or all promotional copy.

## 1. Classify the scenario before summarizing

For each central claim record `question | verified facts, sources and as-of date | assumptions and unknowns | verdict | next action and reassessment trigger`. Separate factual verification, value judgments and predicted effects. A valid supporting premise does not prove the entire claim or a future outcome. Votes can choose a recommendation; they do not establish facts.

| Evidence state | Verdict and required content |
| :--- | :--- |
| Sufficient evidence supports the full scope | State support within that scope, the action to maintain or take, and the key evidence. |
| Only part is supported or support depends on conditions | Separate supported and unknown parts; give a conditional recommendation and verification method. |
| Reliable evidence contradicts the claim | Reject that claim; state the correction or alternative action and counterevidence. |
| Evidence conflicts | Compare disputed points, source directness, dates and methods; identify what can be decided and how to resolve the conflict. |
| Required evidence is absent | Withhold judgment; specify missing evidence, a verification method and a reassessment trigger. Absence of evidence does not prove falsehood. |

For multiple scenarios distinguish the evidence-supported default from observable conditions that would change it. Do not invent probabilities, effect sizes, owners or deadlines. Distinguish recommended actions from actions already performed.

## 2. Required three sentences

1. **What — verdict:** answer the question directly with adopt, conditionally adopt, reject, withhold judgment or an equally clear conclusion; retain its scope and decisive conditions.
2. **How — action:** state who should do what or which evidence to check by which method; for conditional or withheld judgments include the reassessment trigger without inventing owners or deadlines.
3. **Why — evidence:** connect the key evidence and its limits to the conclusion; make it traceable to sources or evidence identifiers in the body.

Do not merge the three slots into one sentence or substitute headings or noun fragments for complete sentences. Replace “the evidence is valid but uncertain” with what is established and what remains unknown. Clarity never permits deleting uncertainty or making a stronger claim than the evidence supports. Put lengthy citations and supporting detail in the body while retaining decisive conditions, risks and unverified status in the summary.

## 3. Editing and acceptance

After Lead confirms scenario facts and verdicts, Ponytail removes repetition while preserving the three sentences' verdict, action and evidence. Humanizer Editor rewrites in plain language and compares against the source again for the three-sentence structure, numbers, negations, conditions, risks, sources and unknowns. Return new factual or recommendation needs to Lead rather than changing the conclusion during editing.

QA/Test Engineer (Lead may cover small tasks) checks every item:
- Exactly three sentences answering What, How and Why in that order.
- The first identifies the subject and verdict; the second gives an execution or verification method.
- The third matches body evidence, with zero changed facts or omitted decisive conditions after compression.
- Missing, partial, contradictory and conflicting evidence yield neither unsupported certainty nor unsupported false balance.
- Existing verdicts such as security PASS/BLOCKED and all mandatory report fields remain in the body; the summary does not replace review, voting or approval gates.

## 4. Example: partial support

This fictional example illustrates the format; it is not an actual measurement.

Input: caching proposal claims 30% lower API latency; one test shows 200ms → 140ms (evidence T1); production load and error rates are unmeasured.

> Caching reduced latency in one test, but the production adoption decision remains on hold.
> Measure latency and error rates under production-like load, then reassess adoption against acceptance criteria agreed in advance.
> Test T1 reduced latency from 200ms to 140ms, or 30%, but production load and error rates have not been verified.
