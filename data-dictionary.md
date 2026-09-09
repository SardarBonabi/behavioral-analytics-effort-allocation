# Reading the allocation metric

> **Research status and code availability:** The research is currently under review. Full research code and data are proprietary. This document explains the simplified public workflow, not the confidential data schema or final research inclusion rules.

## Unit of observation

The [feature sample](allocation_features.py) expects one row per developer-week, with complete, non-overlapping activity counts. Identifiers and weekly boundaries must be reconciled before this transformation. The function checks duplicate developer-week pairs and rejects missing or negative activity counts; it does not validate collection coverage, identifier completeness, or calendar alignment.

## Input fields

| Field | Meaning in the public sample |
|---|---|
| `developer` | Developer identifier used to distinguish panel rows |
| `week` | Consistently defined weekly period |
| `repositories_created` | Public repository creations |
| `commits` | Public commits |
| `pull_requests` | Public pull requests |
| `reviews` | Public reviews |
| `discussions_started` | Public discussion initiations |
| `discussions_answered` | Public discussion answers |
| `issues` | Public issues |
| `private_contributions` | Available private activity count; does not imply access to private code or its content |

These names describe the representative Python interface. They do not specify original API fields, extraction filters, deduplication rules, or database tables.

## Derived metrics

| Output | Calculation | Interpretation |
|---|---|---|
| `public_contributions` | Sum of the seven public activity counts | Observable public activity volume |
| `total_contributions` | Public + private contributions | Denominator for allocation |
| `public_share` | Public / total when total is positive | Fraction of counted activity that is public, between 0 and 1 |

A zero-total week receives an undefined share (`NaN`) in this sample. A zero public count with positive private activity receives a share of zero. Missing collection records must be resolved before either interpretation is made. Counts do not measure hours, cognitive effort, or equal units of business value.

## Synthetic examples: why the denominator matters

**All numbers below are invented arithmetic examples, not research observations or estimated effects.** Public counts are already aggregated across the seven activity types.

| Example | Public | Private | Total | Public share |
|---|---:|---:|---:|---:|
| Reference | 6 | 4 | 10 | 60% |
| Less public activity | 3 | 4 | 7 | 42.9% |
| More private activity | 6 | 8 | 14 | 42.9% |
| Private activity only | 0 | 4 | 4 | 0% |
| No activity | 0 | 0 | 0 | Undefined |

The same share can arise from different changes in behavior. Report the numerator and denominator components alongside the ratio before attributing a shift to reduced public work.

## Aggregation changes the question

For two synthetic developer-weeks with public/total counts of 1/1 and 0/9, the mean of individual shares is **50%**, while the pooled share is **10%**. The former weights each eligible developer-week equally; the latter weights by activity volume. Neither descriptive summary is the study's adjusted causal estimate. Choose the aggregation to match the product question and state its weighting explicitly.

Likewise, a **3% relative decrease** from a hypothetical 60% baseline gives 58.2%, a **1.8-percentage-point** decrease. The baseline here is invented; it is not a reported study baseline. See [effect interpretation](effect_interpretation.py) and [methodology](methodology.md) for the distinction between arithmetic and causal inference.
