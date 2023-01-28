from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # knight or knave but not both
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    # knight speaks always truth
    Implication(AKnight, And(AKnight, AKnave)),
    # knabe always lies
    Implication(AKnave, Not(And(AKnight, AKnave))),
    #And(AKnave, Not(AKnight)),
    #Implication(Not(AKnight), AKnave),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # knight or knave but not both
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    Implication(AKnight, And(AKnave, BKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave))),
)
knowledge1.add(knowledge0)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),

    # Knight say true
    Implication(AKnight, Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave))),
    Implication(BKnight, Or(
        And(AKnight, BKnave),
        And(BKnight, AKnave))),

    # Knave lies (negate)
    Implication(AKnave, Not(Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave)))),
    Implication(BKnave, Not(Or(
        And(AKnight, BKnave),
        And(BKnight, AKnave)))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),

    # B says
    Implication(BKnight, And(Implication(AKnight, AKnave),
                            Implication(AKnave, Not(AKnave)))),
    Implication(BKnight, CKnave),

    Implication(BKnave, Not(And(Implication(AKnight, AKnave),
                            Implication(AKnave, Not(AKnave))))),
    Implication(BKnave, Not(CKnave)),

    # C says
    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),
)



def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
