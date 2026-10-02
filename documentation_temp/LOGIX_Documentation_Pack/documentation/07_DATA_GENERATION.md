# Data Generation

## Generator
Primary master generator: `python/generators/master_data.py`

Transactional generators are maintained under `python/generators/transactional/`.

## Synthetic Data Rules
- Geography: India
- Currency: INR
- Date range: 2023-01-01 to 2025-12-31
- Random seed: 42
- Valid PK/FK relationships
- Controlled missingness
- Business-oriented status transitions
- Realistic logistics attributes

## Raw Data
Final datasets are stored under `data/raw/`.

## Reproducibility
Generation uses deterministic random seeds so the synthetic dataset can be regenerated consistently when generator configuration is unchanged.
