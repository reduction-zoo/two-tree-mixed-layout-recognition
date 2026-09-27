# 3-SAT → Mixed-layout recognition of 2-trees campaign state

Status: Prepare partial; the finite target fixtures lack a NO-SOLUTION 2-tree. No reduction or solution is claimed.

Initial setup: this pass built the testing foundation and ran no construction rounds. Future work follows the current user's scope and pipeline.

Capability probe: CPython 3.12.14, locked `z3-solver` 4.16.0.0. SAT and 2-tree layout encodings passed direct witness validation and finite exhaustive crosschecks. No target negative instance is yet in the finite fixture set. See [preparation.md](work/preparation.md).

Next action: enlarge target negative coverage, then construct and review a reduction under the [contract](work/contract.md) in a later research campaign. The 120 source cases are fixed before construction.

| ID | Attempted mechanism or literature scope | First check | Outcome | Evidence |
|---|---|---|---|---|
