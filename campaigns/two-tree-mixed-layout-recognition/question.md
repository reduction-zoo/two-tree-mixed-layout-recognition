# 3-SAT → Mixed-layout recognition of 2-trees

Category: Complexity open

## Source

A source instance is an explicitly encoded Boolean formula with at most three literals per clause. Its outputs are satisfying Boolean assignments, or NO-SOLUTION when the formula is unsatisfiable.

## Target

The target must be a 2-tree and asks for a vertex order with one stack and one queue. Independent stack edges may not alternate and independent queue edges may not nest. A 2-tree starts from an edge and repeatedly adds a vertex adjacent to both endpoints of an existing edge.

## Required result

Construct deterministic polynomial-time maps F and G: F sends every legal source instance to a legal target instance, and G(x,y) is a valid source output for every valid output y of F(x). Preserve the stated threshold, domain and promises. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The question asks whether choosing a mixed layout is hard even on a narrowly structured graph class.

## Difficulty

Fixed-order page assignment is tractable. The unresolved work is forcing orders while maintaining the 2-tree structure.

## Literature context

The cited work retains recognition of one-stack, one-queue layouts on 2-trees. Counterexamples to universal existence do not establish recognition hardness.

Literature checked 2026-09-15. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [On Mixed Linear Layouts of Series-Parallel Graphs](https://arxiv.org/pdf/2008.10475): - R5: On Mixed Linear Layouts of Series-Parallel Graphs, Section 3, PDF page 7, TCS (2022); Pupyrev's author-maintained agenda, mixed-layout recognition section, inspected September 14, 2026.
- [Pupyrev's author-maintained agenda](https://spupyrev.github.io/layoutproblems.html): - R5: On Mixed Linear Layouts of Series-Parallel Graphs, Section 3, PDF page 7, TCS (2022); Pupyrev's author-maintained agenda, mixed-layout recognition section, inspected September 14, 2026.

Fixed from board record `website/questions/two-tree-mixed-layout-recognition.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
