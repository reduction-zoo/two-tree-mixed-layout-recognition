# Prepared contract

Source: `{"num_vars":n,"clauses":[[signed_literal,...],...]}` with at most three literals per clause. Output a satisfying Boolean `{"assignment":[...]}` or `{"status":"NO-SOLUTION"}`.

Target: `{"vertices":n,"edges":[[u,v],...]}` for a simple 2-tree, `n>=2`. A 2-tree starts with one edge and repeatedly adds a vertex adjacent to both ends of an existing edge. A positive output `{"order":[vertex,...],"pages":[0_or_1_by_edge,...]}` gives a vertex permutation and a page for each input edge in input order. Page 0 is a stack: independent edges may not alternate. Page 1 is a queue: independent edges may not nest. `NO-SOLUTION` is valid iff no mixed layout exists.

`algorithm.py` reads source JSON from stdin and emits legal target JSON. `algorithm.py --extract` reads `{"source":source,"target_solution":output}` and emits a valid source output. Both commands are deterministic, polynomial time, independent subprocesses. Errors exit nonzero; diagnostics go to stderr. Recovery must handle every valid target output.
