

import json
from eff_lookup import SequenceDatabase, OrfFinder

def test(solution, test_cases):
    print("\nTESTING %s\n" % solution.__name__)
    correct_count = 0
    for inp,out in test_cases:
        correct, got = solution(*inp, out)
        if correct:
            correct_count += 1
        
        else:
            print("inp:", inp)
            print("out:", out)
            print("got:", got)
            print()
    print("passed %d/%d tests\n" % (correct_count, len(test_cases)))

def sd_solution(sequences, query, out):
    sd = SequenceDatabase()
    for seq in sequences:
        sd.addSequence(seq)
    got = sd.query(query)
    correct = got == out
    return correct, got

with open("sd_test_cases.json", "r") as f:
    test_cases = json.load(f)
    test(sd_solution, test_cases)

def of_solution(genome, start, end, out):
    of = OrfFinder(genome)
    got = of.find(start, end)
    correct = sorted(got) == sorted(out)
    return correct, got

with open("of_test_cases.json", "r") as f:
    test_cases = json.load(f)
    test(of_solution, test_cases)


