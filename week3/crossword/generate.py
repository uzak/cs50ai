import sys

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

from crossword import *

class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        # for k in sorted(self.domains, key=lambda x: x.i**3 + x.j**2 + len(x.direction)):
        #     v = self.domains[k]
        #     print(f"{str(k):20} {len(v)}")
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var, words in self.domains.items():
            self.domains[var] = set(filter(lambda x: len(x) == var.length, words))

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # print("revise", x, y)
        revised = False
        revised_words = [word for word in self.domains[x]]    # copy
        for word_x in self.domains[x]:
            idx = self.crossword.overlaps[(x, y)]
            if idx is None:
                continue
            word_y_matches = [word_x[idx[0]] == word_y[idx[1]] for word_y in self.domains[y]]
            # print("XXX", word_x, any(word_y_matches), idx, self.domains[y])
            if not any(word_y_matches):
                revised_words.remove(word_x)
                revised = True
        # print("revised words", x, set(self.domains[x]) - set(revised_words))
        self.domains[x] = revised_words
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # print("arcs", arcs)
        # print("variables", self.crossword.variables)

        if arcs is None:
            arcs = [(x, y) for (x, y), v in self.crossword.overlaps.items() 
                        if v is not None]

        #XXXXXXXXX
        for (x, y) in arcs:
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z == y:
                        continue
                    #print("XXX adding more", (z, x))
                    arcs.append((z, x))
        #XXXXXXXXX
        # print("arcs", arcs)
        # print(f"{self.domains=}")
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var not in assignment:
                return False
            if len(assignment[var]) == 0:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # print("C", assignment)
        # print("C", self.domains)
        for x, word_x in assignment.items():
            for y, word_y in assignment.items():
                if x == y:
                    continue
                idx = self.crossword.overlaps[(x, y)]
                if idx is None:
                    continue
                matches = word_x[idx[0]] == word_y[idx[1]]
                is_same_words = word_x == word_y
                # print(f"XXX {matches} {word_x=}, {word_y=}, {idx=}, {x}, {y}")
                if not matches or is_same_words:
                    return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        return self.domains[var]

        conflicts = {}
        for word in self.domains[var]:
            nok = 0
            for n in self.crossword.neighbors(var):
                for word_n in self.domains[n]:
                    assignment_ = {n: word_n, var: word}
                    if not self.consistent(assignment_):
                        nok += 1
            conflicts[word] = nok 
        # for (k, _) in sorted(conflicts.items(), key=lambda x: x[1]):
        #     v = conflicts[k]
        #     print(k, v)
        return [k for k, _ in sorted(conflicts.items(), key=lambda x: x[1])]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = [var for var in self.crossword.variables 
                        if var not in assignment]
        values_remaining = [(var, len(self.domains[var])) for var in unassigned]
        min_remaining = min([length for (_, length) in values_remaining])
        # print(values_remaining)
        values_remaining = [var for (var, length) in values_remaining 
                            if length == min_remaining]
        if len(values_remaining) == 1:
            return values_remaining[0]
        else:
            # choose highest degree
            overlaps = [(x, y) for (x, y), v in self.crossword.overlaps.items() 
                        if v is not None and x in values_remaining]
            overlaps_len = {}
            for (x, _) in overlaps:
                overlaps_len[x] = len([x2 for (x2, _) in overlaps if x == x2])
                overlaps_sorted = sorted(overlaps_len.items(), key=lambda x: x[1], reverse=True)
                # print("overlaps_sorted", overlaps_sorted)
                return overlaps_sorted[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # print(f"{assignment=}")
        # print(f"{self.domains=}")

        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for word in self.order_domain_values(var, assignment):
            # print(f"{var=}, {word=}")
            assignment[var] = word
            if self.consistent(assignment):
                # print("consistent", var, word)
                result = self.backtrack(assignment)
                if result:
                    return result
            del assignment[var]


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
