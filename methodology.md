# Effort allocation and project choice

## Outcome construction

Public contribution aggregates seven activity types: repository creation, commits, pull requests, reviews, discussion initiation, discussion answers, and issues. Public share is public contribution divided by public plus private contribution. Counts are behavioral proxies, not observed hours of effort. Private activity measures do not imply access to private code content.

The public sample marks zero-total weeks as undefined shares. This is an explicit illustrative denominator policy; the final research inclusion rules are not distributed. Incomplete collection records must be distinguished from true inactivity before aggregation.

## Causal analysis

The research uses matched difference-in-differences around Italy's access suspension, with France and Portugal as controls. Developer and week fixed effects and developer-clustered standard errors structure the panel analysis. The manuscript uses a Poisson framework and reports incidence-rate ratios. The public sample focuses on feature logic and interpretation rather than reimplementing the estimator.

The approximately 3% relative decrease in public share should be interpreted alongside changes in public and private contribution. A ratio alone cannot identify which component moved. Activity-level decomposition links the aggregate shift to codification-intensive contributions.

## Conditional choice

The completed project-entry analysis uses a user-project-week panel and conditional logistic regression. A useful specification must define the eligible alternatives, decision timing, conditioning groups, and treatment interactions. The representative sample uses developer-week groups. Variables constant within such a group are not separately identified; interactions with project-varying features are needed to study changes in relative preference. This example is not a recovered specification of the original causal entry model.

Groups with no outcome variation do not identify conditional-logit coefficients. Excluding these groups changes the population supporting the estimate. A project set built from future behavior can leak the outcome into the alternatives and should be avoided.

### Synthetic example: which comparisons identify the model?

The following example illustrates the filtering logic in [project_entry.py](project_entry.py). All identifiers and values are synthetic; they are not research observations or fitted results. Each developer-week has two eligible projects defined before the decision.

| Developer-week | Project | Entered | Project feature | Access interruption |
|---|---|---:|---:|---:|
| A, week 1 | X | 1 | 2 | 1 |
| A, week 1 | Y | 0 | 5 | 1 |
| B, week 1 | X | 0 | 2 | 0 |
| B, week 1 | Y | 0 | 5 | 0 |
| C, week 1 | X | 1 | 2 | 1 |
| C, week 1 | Y | 1 | 5 | 1 |

Only developer A's group has both outcomes and survives this sample's within-group variation filter. B's all-zero group and C's all-one group do not contribute to conditional coefficient estimation. One informative group is insufficient for a credible empirical model; this table demonstrates eligibility only.

The project feature varies within A's group, while the access-interruption indicator does not. A standalone interruption coefficient therefore cannot be estimated with developer-week conditioning. An interruption-by-project-feature interaction varies across alternatives, but within-group variation alone does not guarantee identification: the full design must also have independent regressors and sufficient variation across groups. In this tiny example, the interaction equals the project feature in the only retained group, so their coefficients cannot be separately identified.

**Product interpretation:** this sample compares project selection within informative developer-weeks. It does not by itself estimate whether AI access makes an otherwise inactive user enter any project. That overall participation question remains distinct from the conditional choice comparison and requires the appropriate causal outcome analysis.

## Interpretation

The research connects reduced public contribution with changes in cross-project breadth and developer experience. It does not equate all public events with equal effort or value. The business relevance is metric decomposition: distinguish overall activity, allocation, and entry into new opportunities before drawing conclusions about engagement.
