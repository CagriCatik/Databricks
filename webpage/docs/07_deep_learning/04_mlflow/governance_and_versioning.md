# Governance and Versioning

Governance ensures that models are deployed responsibly and can be audited.

## Versioning

- Treat each training run as immutable and record the exact code, data version, and configuration.
- Use semantic versioning or a simple numeric scheme for registered model versions.

## Approval workflow

- Define checks that must pass before a model can move to Production, for example:
  - Minimum performance thresholds.
  - Bias and fairness checks where relevant.
  - Security and compliance review.

## Auditability

- Record who approved stage transitions in the Model Registry.
- Preserve key artifacts such as evaluation reports and data summaries.

Governance practices help ensure that the system remains trustworthy as models evolve.
