# actions-dynamic-matrix-testing

Repo for testing/prototyping dynamic matrix CI

2 build matrices are defined in `.github/matrices.yaml`:

- `quick` containing a small matrix for "regular" CI
- `full` containing a large matrix, for full/thorough CI

The workflow `dynamic.yml` is triggered by several events.