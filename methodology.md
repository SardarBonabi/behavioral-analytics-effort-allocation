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

## Interpretation

The research connects reduced public contribution with changes in cross-project breadth and developer experience. It does not equate all public events with equal effort or value. The business relevance is metric decomposition: distinguish overall activity, allocation, and entry into new opportunities before drawing conclusions about engagement.
