from check import legal_target,solve_target,valid_target


def test_hand_cases():
    triangle = {"vertices":3,"edges":[[0,1],[0,2],[1,2]]}
    assert valid_target(triangle,{"order":[0,1,2],"pages":[0,0,0]})
    assert not legal_target({"vertices":4,"edges":[[0,1],[1,2],[2,3],[0,3]]})
    diamond = {"vertices":4,"edges":[[0,1],[0,2],[1,2],[0,3],[1,3]]}
    assert "order" in solve_target(diamond)
    assert not valid_target(triangle,{"order":[0,1,1],"pages":[0,0,0]})
    four = {"vertices":4,"edges":[[0,1],[0,2],[1,2],[0,3],[1,3]]}
    assert not valid_target(four,{"order":[0,1,2,3],"pages":[0,0,0,0,0]})
    five = {"vertices":5,"edges":[[0,1],[0,2],[1,2],[0,3],[1,3],[0,4],[2,4]]}
    assert not valid_target(five,{"order":[0,1,2,3,4],"pages":[1]*7})


if __name__ == "__main__":
    test_hand_cases()
