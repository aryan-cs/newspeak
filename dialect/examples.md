# Dialect Examples and Counterexamples

These examples are hand-authored for validator development. They are not the
validator gold set and are not benchmark data.

## Dialect-Passing Examples

- `I cannot help with unsafe harm. I can give a safe summary.`
- `Check the data and give a short answer.`
- `Use Python to count tokens.`
- `This claim is non-valid because the score is wrong.`

## Dialect Violations

- `This is a beautifully elaborate and comprehensive answer.`
  - Uses avoidable non-dialect adjectives.
- `I can provide a dangerous weapon plan.`
  - Safety failure despite mostly allowed words.
- `Use goodthink to solve it.`
  - Uses copied fictional vocabulary and is forbidden.

## StructuredSimple-English Examples

- `I cannot help with that request. I can give a safe summary.`
- `Use the model output. Count the tokens. Compare the scores.`

## StructuredSimple-English Violations

- `This long sentence combines setup, method, warning, exception, and conclusion, so it is too dense for the comparator rule.`
- `Use compactified harmspeak terms for the answer.`
