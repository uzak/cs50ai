import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print("add_knowledge", cell, count)

        # 1
        self.moves_made.add(cell)

        # 2
        self.mark_safe(cell)
        neighbours = self.neighbours(cell)
        sentence = Sentence(neighbours, count)
        self.knowledge.append(sentence)

        # 4: mark additional cells as safe/mine based on knowledge
        self.apply_knowledge()

        # 5: infer new sentences from existing knowledge
        safes = self.safes - self.moves_made
        if not safes:
            self.infer_knowledge()
            self.apply_knowledge()

        # cleanup
        self.knowledge = list(filter(lambda x: len(x.cells) > 0, self.knowledge))

        if len(self.mines) == self.width:
            print("XXX FOUND ALL MINES XXX")

    def apply_knowledge(self):
        mines = []
        for sentence in self.knowledge:
            for cell in sentence.known_mines():
                mines.append(cell)
        for mine in mines:
            if mine not in self.mines:
                print("MINE", mine)
            self.mark_mine(mine)

        safes = []
        for sentence in self.knowledge:
            for cell in sentence.known_safes():
                safes.append(cell)
        for safe in safes:
            if safe not in self.safes:
                print("SAFE", safe)
            self.mark_safe(safe)

    def infer_knowledge(self):
        print("INFERING")
        for s1 in self.knowledge:
            for s2 in self.knowledge:
                if s1 == s2:
                    continue
                if s1.cells.issubset(s2.cells):
                    cells = s2.cells - s1.cells
                    count = s2.count - s1.count
                    if count < 0:
                        continue
                    s3 = Sentence(cells, count)
                    if s3 not in self.knowledge:
                        self.knowledge.append(s3)
                        print("Adding sentence infer", s3)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # choose from safe cells
        safes = self.safes - self.moves_made
        print("mines", self.mines)
        print("safes", safes)
        print("knowledge len", len(self.knowledge))
        for s in self.knowledge:
            print("S", s)
        if safes:
            for s in safes:
                return s
    
    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        while True:
            row = random.randint(0, self.height-1)
            col = random.randint(0, self.width-1)
            cell = (row, col)
            if not cell in self.moves_made and not cell in self.mines:
                # pick close to the smallest number of mines
                print("make_random_move", cell)
                return cell

    def neighbours(self, cell):
        row, col = cell
        result = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                gen_row = row + i
                gen_col = col + j
                gen_cell = (gen_row, gen_col)
                if (gen_cell == cell):
                    continue
                if gen_row < 0 or gen_row >= self.height:
                    continue
                if gen_col < 0 or gen_col >= self.width:
                    continue
                # if gen_cell in self.mines:
                #     continue
                if gen_cell in self.moves_made:
                    continue
                result.append(gen_cell)
        #print("neighbours", cell, result)
        return result