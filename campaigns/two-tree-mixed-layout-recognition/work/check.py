"""Independent 3-SAT and split-graph star-coloring oracles."""

import argparse
import json
import subprocess
import sys
from itertools import combinations, permutations, product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source, dict):
        return False
    n = source.get("num_vars")
    clauses = source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses, list)
            and all(isinstance(clause, list) and len(clause) <= 3
                    and all(type(literal) is int and 1 <= abs(literal) <= n for literal in clause)
                    for clause in clauses))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal source formula")
    variables = [z3.Bool(f"x{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Or(*(variables[abs(literal) - 1] if literal > 0
                           else z3.Not(variables[-literal - 1]) for literal in clause)))
    result = solver.check()
    if result == z3.unsat:
        return {"status": "NO-SOLUTION"}
    if result != z3.sat:
        raise RuntimeError(f"Inconclusive source solver: {result}")
    model = solver.model()
    return {"assignment": [z3.is_true(model.eval(variable, model_completion=True)) for variable in variables]}


def valid_source(source, output):
    if not legal_source(source) or not isinstance(output, dict):
        return False
    if output == {"status": "NO-SOLUTION"}:
        return solve_source(source) == output
    assignment = output.get("assignment")
    if set(output) != {"assignment"} or not isinstance(assignment, list) or len(assignment) != source["num_vars"] or any(type(value) is not bool for value in assignment):
        return False
    return all(any(assignment[abs(literal) - 1] == (literal > 0) for literal in clause)
               for clause in source["clauses"])


def legal_target(target):
    if not isinstance(target,dict) or set(target) != {"vertices","edges"}:
        return False
    n,edges = target["vertices"],target["edges"]
    if (type(n) is not int or n < 2 or not isinstance(edges,list)
            or len(edges) != 2*n-3
            or any(not isinstance(edge,list) or len(edge) != 2
                   or any(type(v) is not int or not 0 <= v < n for v in edge)
                   or edge[0] >= edge[1] for edge in edges)
            or len({tuple(edge) for edge in edges}) != len(edges)):
        return False
    adjacent = [set() for _ in range(n)]
    for u,v in edges:
        adjacent[u].add(v)
        adjacent[v].add(u)
    remaining = set(range(n))
    while len(remaining) > 2:
        leaf = next((v for v in remaining if len(adjacent[v] & remaining) == 2
                     and all(b in adjacent[a] for a,b in combinations(adjacent[v] & remaining,2))),None)
        if leaf is None:
            return False
        remaining.remove(leaf)
    a,b = tuple(remaining)
    return b in adjacent[a]


def independent_pairs(target):
    for i,j in combinations(range(len(target["edges"])),2):
        u,v = target["edges"][i]
        x,y = target["edges"][j]
        if len({u,v,x,y}) == 4:
            yield i,j,(u,v),(x,y)


def direct_layout(target,order,pages):
    n,m = target["vertices"],len(target["edges"])
    if (not isinstance(order,list) or len(order) != n
            or any(type(v) is not int for v in order)
            or sorted(order) != list(range(n))
            or not isinstance(pages,list) or len(pages) != m
            or any(type(p) is not int or p not in (0,1) for p in pages)):
        return False
    position = {v:i for i,v in enumerate(order)}
    for i,j,(u,v),(x,y) in independent_pairs(target):
        a,b = sorted((position[u],position[v]))
        c,d = sorted((position[x],position[y]))
        if pages[i] == pages[j] == 0 and (a<c<b<d or c<a<d<b):
            return False
        if pages[i] == pages[j] == 1 and (a<c<d<b or c<a<b<d):
            return False
    return True


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Target graph is not a 2-tree")
    n,m = target["vertices"],len(target["edges"])
    position = [z3.Int(f"pos_{v}") for v in range(n)]
    stack = [z3.Bool(f"stack_{e}") for e in range(m)]
    solver = z3.Solver()
    solver.add(z3.Distinct(position))
    for p in position:
        solver.add(p >= 0,p < n)
    for i,j,(u,v),(x,y) in independent_pairs(target):
        a,b = z3.If(position[u]<position[v],position[u],position[v]),z3.If(position[u]<position[v],position[v],position[u])
        c,d = z3.If(position[x]<position[y],position[x],position[y]),z3.If(position[x]<position[y],position[y],position[x])
        alternate = z3.Or(z3.And(a<c,c<b,b<d),z3.And(c<a,a<d,d<b))
        nested = z3.Or(z3.And(a<c,c<d,d<b),z3.And(c<a,a<b,b<d))
        solver.add(z3.Not(z3.And(stack[i],stack[j],alternate)))
        solver.add(z3.Not(z3.And(z3.Not(stack[i]),z3.Not(stack[j]),nested)))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive layout solver: {result}")
        model = solver.model()
        positions = [model.eval(p).as_long() for p in position]
        order = sorted(range(n),key=lambda v:positions[v])
        pages = [0 if z3.is_true(model.eval(s,model_completion=True)) else 1 for s in stack]
        assert direct_layout(target,order,pages)
        outputs.append({"order":order,"pages":pages})
        solver.add(z3.Or(*([p != positions[v] for v,p in enumerate(position)]
                           +[s != (pages[i] == 0) for i,s in enumerate(stack)])))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return (set(output) == {"order","pages"}
            and direct_layout(target,output["order"],output["pages"]))


def exhaustive_target(target):
    n,m = target["vertices"],len(target["edges"])
    for order in permutations(range(n)):
        for pages in product((0,1),repeat=m):
            if direct_layout(target,list(order),list(pages)):
                return {"order":list(order),"pages":list(pages)}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases
    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for n,clauses,answer in EDGE_CASES:
        assert ("assignment" in solve_source({"num_vars":n,"clauses":clauses})) == answer
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exists = any(all(any(bits[abs(lit)-1] == (lit > 0) for lit in clause)
                             for clause in source["clauses"])
                     for bits in product((False,True),repeat=source["num_vars"]))
        assert ("assignment" in current) == exists == ("assignment" in case["expected"])
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    import random
    checked = 0
    for seed in range(75):
        rng = random.Random(seed)
        n = rng.randint(2,5)
        edges = [[0,1]]
        for v in range(2,n):
            a,b = rng.choice(edges)
            edges += [[min(v,a),max(v,a)],[min(v,b),max(v,b)]]
        target = {"vertices":n,"edges":edges}
        assert legal_target(target)
        assert ("order" in solve_target(target)) == ("order" in exhaustive_target(target))
        checked += 1
    print(f"Self-test passed: {len(cases)} source formulas and {checked} exhaustively checked 2-trees")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal 2-tree target: {target}")
        for output in target_solutions(target):
            assert valid_target(target,output)
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
