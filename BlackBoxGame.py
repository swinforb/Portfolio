# Author: Ben Swinford
# Date: 08/04/20
# Description: Runs the Black Box game, performing checks in each possibility to see which "shots" have hits or
# reflections. The score is kept track through remembering previous guess and subtracting points for each entry, exit,
# and incorrect guess.


class BlackBoxGame:
    """
    Runs the entire black box game, it's functions create a 10x10 board and takes coordinates as
    parameters for atoms as well as shot coordinates. The end result of this class should be a
    basic version of the Black Box Game. This code follows each of the rules found on wikipedia.
    does not communicate with other classes
    """
    def __init__(self, _atom_locations):
        """
        initializes each data type used,
        provides data types for: atom_locations, reflect_locations
                                score, atom_amount, and the board
        """
        self._atom_locations = _atom_locations
        self._score = 26
        self._atom_amount = 4
        self._row_amt = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self._board = []
        self._previous_shots = []
        # accessible atom locations
        self._atom_row = []
        self._atom_column = []
        # reflection locations
        self._row_reflect_1 = []
        self._col_reflect_1 = []
        self._row_reflect_2 = []
        self._col_reflect_2 = []
        self._row_reflect_3 = []
        self._col_reflect_3 = []
        self._row_reflect_4 = []
        self._col_reflect_4 = []

    def create_board(self):
        """
        Creates a list of lists to serve as the board
        """
        row = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for column in range(len(row)):
            self._board.append(row)

    def get_board(self):
        """
        Returns the current state of the board
        """
        return self._board

    def check_valid_shot(self, row, column):
        """
        Returns False if parameters would be a corner on the board or not on the edge,
        Otherwise returns True
        """
        # If it is a corner
        if row == 0 or row == 9:
            if column == 0 or column == 9:
                return False
        # If the shot / grid is in the grid
        if row != 0 and row != 9:
            if column != 0 and column != 9:
                return False
        if column != 0 and column != 9:
            if row != 0 and row != 9:
                return False
        return True

    def enter_atoms_to_board(self):
        """
        Stores the atom locations into lists easier to access
        """
        self._atom_row.clear()
        self._atom_column.clear()
        # stores it to accessible atom locations
        for items in range(len(self._atom_locations)):
            tupl3 = self._atom_locations[items]
            self._atom_row.append(tupl3[0])
            self._atom_column.append(tupl3[1])

    def reflections(self, row, col):
        """
        Creates separate lists for the reflection points to be referenced later,
        i.e. the corners of each atom
        """
        # for x in range(len(self._atom_row)):
        if self._atom_row[row] - 1 != 0:
            # top left reflection
            if self._atom_column[col] - 1 != 0:
                self._row_reflect_1.append(self._atom_row[row]-1)
                self._col_reflect_1.append(self._atom_column[col]-1)
            # bottom left reflection
            if self._atom_column[col] + 1 != 9:
                self._row_reflect_3.append(self._atom_row[row]-1)
                self._col_reflect_3.append(self._atom_column[col]+1)
        if self._atom_row[row] + 1 != 9:
            # top right reflection
            if self._atom_column[col] - 1 != 0:
                self._row_reflect_2.append(self._atom_row[row]+1)
                self._col_reflect_2.append(self._atom_column[col]-1)
            # bottom right reflection
            if self._atom_column[col] + 1 != 9:
                self._row_reflect_4.append(self._atom_row[row]+1)
                self._col_reflect_4.append(self._atom_column[col]+1)



    def alter_z(self, z, what_hit, distance_traveled):
        """
        Alterations to the list z in order to compress the "first_hit" runs
        """
        z.clear()
        z.append(what_hit)
        z.append(distance_traveled-1)
        return z

    # first_hit section runs the code for going left, right, up, or down, looks to see if any hits are made
    # if starting_row == 0:  going down column  , x = 9
    def first_hit_left_row(self, starting_column, z, x, prev):
        """
        Goes down the column, returns the closest reflection, atom, or edge
        """
        for distance_traveled in self._row_amt:
            for atom in range(len(self._atom_locations)):
                # atom hits
                if distance_traveled-1 == self._atom_row[atom-1]:  # looks at each atom
                    if starting_column == self._atom_column[atom-1]:  # if the column matches any atom for the row
                        if x > distance_traveled-1 > prev:
                            x = distance_traveled - 1
                            z = self.alter_z(z, 11, distance_traveled)
                # reflection hits
                if atom < len(self._row_reflect_1):
                    if distance_traveled-1 == self._row_reflect_1[atom-1]:
                        if starting_column == self._col_reflect_1[atom-1]:
                            if x > distance_traveled-1 > prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 1, distance_traveled)
                if atom < len(self._col_reflect_3):
                    if distance_traveled-1 == self._row_reflect_3[atom-1]:
                        if starting_column == self._col_reflect_3[atom-1]:
                            if x > distance_traveled-1 > prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 3, distance_traveled)
        if x == 9:
            z.append(9)
            z.append(1)
        return z

    # if starting_row == 9:  going up column  , x = 0
    def first_hit_right_row(self, starting_column, z, x, prev):
        """
        Goes up the column, returns the closest reflection, atom, or edge
        """
        for distance_traveled in self._row_amt:
            for atom in range(len(self._atom_locations)):
                # atom hits
                if distance_traveled-1 == self._atom_row[atom-1]:
                    if starting_column == self._atom_column[atom-1]:  # check to see if hit
                        if x < distance_traveled-1 < prev:
                            x = distance_traveled - 1
                            z = self.alter_z(z, 11, distance_traveled)
                # reflection hits
                if atom < len(self._row_reflect_2):
                    if distance_traveled-1 == self._row_reflect_2[atom-1]:
                        if starting_column == self._col_reflect_2[atom-1]:  # check to see if hit
                            if x < distance_traveled-1 < prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 2, distance_traveled)
                if atom < len(self._col_reflect_4):
                    if distance_traveled-1 == self._row_reflect_4[atom-1]:
                        if starting_column == self._col_reflect_4[atom-1]:  # check to see if hit
                            if x < distance_traveled-1 < prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 4, distance_traveled)
        if x == 0:
            z.append(0)
            z.append(1)
        return z

    # if starting_col == 0:  going right row , x = 9
    def first_hit_top_col(self, starting_row, z, x, prev):
        """
        Goes right on the row, returns the closest reflection, atom, or edge
        """
        for distance_traveled in self._row_amt:
            for atom in range(len(self._atom_locations)):
                # atom hits
                if distance_traveled-1 == self._atom_column[atom-1]:
                    if starting_row == self._atom_row[atom-1]:
                        if x > distance_traveled-1 > prev:
                            x = distance_traveled - 1
                            z = self.alter_z(z, 11, distance_traveled)
                # reflection hits
                if atom < len(self._col_reflect_1):
                    if distance_traveled-1 == self._col_reflect_1[atom-1]:  # hits each one
                        if starting_row == self._row_reflect_1[atom-1]:  # then compares it to see if one is in this col
                            if x > distance_traveled-1 > prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 1, distance_traveled)
                if atom < len(self._row_reflect_2):
                    if distance_traveled-1 == self._col_reflect_2[atom-1]:
                        if starting_row == self._row_reflect_2[atom-1]:
                            if x > distance_traveled-1 > prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 2, distance_traveled)
        if x == 9:
            z.append(9)
            z.append(0)
        return z

    # if starting_col == 9:  going left row , x = 0
    def first_hit_bottom_col(self, starting_row, z, x, prev):
        """
        Goes left on the row, returns the closest reflection, atom, or edge
        """
        for distance_traveled in self._row_amt:
            for atom in range(len(self._atom_locations)):
                # atom hits
                if distance_traveled-1 == self._atom_column[atom-1]:
                    if starting_row == self._atom_row[atom-1]:  # check to see if hit
                        if x < distance_traveled < prev:
                            x = distance_traveled-1
                            z = self.alter_z(z, 11, distance_traveled)
                # reflection hits
                if atom < len(self._col_reflect_3):
                    if distance_traveled-1 == self._col_reflect_3[atom-1]:
                        if starting_row == self._row_reflect_3[atom-1]:  # check to see if hit
                            if x < distance_traveled-1 < prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 3, distance_traveled)
                if atom < len(self._row_reflect_4):
                    if distance_traveled-1 == self._col_reflect_4[atom-1]:
                        if starting_row == self._row_reflect_4[atom-1]:  # check to see if hit
                            if x < distance_traveled-1 < prev:
                                x = distance_traveled - 1
                                z = self.alter_z(z, 4, distance_traveled)
        if x == 0:
            z.append(0)
            z.append(0)
        return z

#  hit = [what it hit, distance, start at 0 / 9]
    def run_top_left(self, row, col, hit, z):
        """
        If this reflection is hit it will run the corresponding
        function to change the shot's direction
        """
        if hit[2] == 0:
            col_1 = hit[1]
            hit = self.first_hit_bottom_col(hit[1], z, 0, col)  # down to left
            hit.append(3)  # remember direction
            return self.hit_something(hit[1], col_1, hit)
        elif hit[2] == 2:
            row_1 = hit[1]
            hit = self.first_hit_right_row(hit[1], z, 0, row)  # right to up
            hit.append(1)  # remember direction
            return self.hit_something(row_1, hit[1], hit)

    def run_bottom_left(self, row, col, hit, z):
        """
        If this reflection is hit it will run the corresponding
        function to change the shot's direction
        """
        if hit[2] == 1:
            col_1 = hit[1]
            hit = self.first_hit_bottom_col(hit[1], z, 0, col)  # up to left
            hit.append(3)  # remember direction
            return self.hit_something(hit[1], col_1, hit)
        elif hit[2] == 2:
            row_1 = hit[1]
            hit = self.first_hit_left_row(hit[1], z, 9, row)  # right to down
            hit.append(0)  # remember direction
            return self.hit_something(row_1, hit[1], hit)

    def run_top_right(self, row, col, hit, z):
        """
        If this reflection is hit it will run the corresponding
        function to change the shot's direction
        """
        if hit[2] == 0:
            col_1 = hit[1]
            hit = self.first_hit_top_col(hit[1], z, 9, col)  # down to right
            hit.append(2)  # remember direction
            return self.hit_something(hit[1], col_1, hit)
        elif hit[2] == 3:
            row_1 = hit[1]
            hit = self.first_hit_right_row(hit[1], z, 0, row)  # left to up
            hit.append(1)  # remember direction
            return self.hit_something(hit[1], row_1, hit)  # swapped hit1 and row1

    def run_bottom_right(self, row, col, hit, z):
        """
        If this reflection is hit it will run the corresponding
        function to change the shot's direction
        """
        if hit[2] == 1:
            col_1 = hit[1]
            hit = self.first_hit_top_col(hit[1], z, 9, col)  # up to right  # row was col
            hit.append(2)  # remember direction
            return self.hit_something(hit[1], col_1, hit)
        elif hit[2] == 3:
            row_1 = hit[1]
            hit = self.first_hit_left_row(hit[1], z, 9, row)  # right to down
            hit.append(0)  # remember direction
            return self.hit_something(row_1, hit[1], hit)

    def hit_something(self, row, col, hit):
        """
        If a reflection or atom was hit the corresponding function runs
        Returns the ending coordinates
        """
        z = [0]
        # hit[0] remembers if an atom or reflection was hit, and which one
        if hit[0] == 1:
            return self.run_top_left(row, col, hit, z)
        elif hit[0] == 2:
            return self.run_bottom_left(row, col, hit, z)
        elif hit[0] == 3:
            return self.run_top_right(row, col, hit, z)
        elif hit[0] == 4:
            return self.run_bottom_right(row, col, hit, z)
        elif hit[0] == 11:
            return None
        # if there was no hit, returns exit point
        elif hit[0] == 0:
            if hit[1] == 9:
                if hit[2] == 0:
                    return col, hit[1]
                    #return hit[1], col
                if hit[2] == 1:
                    return hit[1], row
                    #return row, hit[1]
            if hit[1] == 0:
                if hit[2] == 0:
                    return col, hit[1]
                    #return hit[1], col
                if hit[2] == 1:
                    return hit[1], row
                    #return row, hit[1]



    # this is the one that runs 3 times for top, middle, bottom
    def shoot_the_shot(self, row, column, z, x):  # SET UP X SO IT IS MANIPULABLE
        """
        Determines which edge the shot is coming from and runs the
        corresponding function, returns the end location after reflections
        """
        # z = [0]
        hit = []
        if row == 0:
            hit = self.first_hit_left_row(column, z, x, -1)    # NEED TO ADJUST OTHER FUNCTION FOR THIS
            if hit[0] == 0:
                return 9, column
            hit.append(0)
        if row == 9:
            hit = self.first_hit_right_row(column, z, x, 10)   # up
            if hit[0] == 0:
                return 0, column
            hit.append(1)
        if column == 0:
            hit = self.first_hit_top_col(row, z, x, -1)   # right     # ALTER X IN OTHER PARAMETERS
            if hit[0] == 0:
                return row, 9
            hit.append(2)
        if column == 9:
            hit = self.first_hit_bottom_col(row, z, x, 10)  # left
            if hit[0] == 0:
                return row, 0
            hit.append(3)
        if hit[0] != 0:
            return self.hit_something(row, column, hit)  # takes in hit as a parameter

    def shoot_ray(self, row, column):
        """
        Parent function that will return if the shot hit, is invalid,
        or where it came out
        """
        z = [0]
        end = 0
        check = self.check_valid_shot(row, column)
        if check is False:
            return False
        if self._score == 26:
            self.enter_atoms_to_board()
            for x in range(len(self._atom_locations)):
                self.reflections(x-1, x-1)
            self._score -= 1
        if row == 9 or column == 9:
            end = 0
        elif row == 0 or column == 0:
            end = 9
        this_shot = row, column
        if this_shot not in self._previous_shots:
            self._score -= 1
            self._previous_shots.append(this_shot)
        result = self.shoot_the_shot(row, column, z, end)
        if result not in self._previous_shots and result is not None:
            self._score -= 1
            # shot_fired = row, column
            # self._previous_shots.append(shot_fired)
            self._previous_shots.append(result)
        return result

        # shoot 3 rays at once, the one that was called, one for above and one for below.
        # the first one to get a 'hit' means the ray actually hit or is reflected (if above / below)
        # if the og and 2 / 3 one hit same time it is just a hit
        # this will be altered for columns / rows ofc
        # if it hits above I can make it go up that column, below goes down the column
        # if it hits left, it goes left on row, if it hits right, it goes right on row
        # if the og shot is a hit, return hit
        # if no more hits, return the exit

        #

    def guess_atom(self, row, column):
        """
        Checks to see if the entered parameters match the coordinates
        of any entered atom, reduces the atoms left by one, reduces
        score if incorrect guess
        Returns True or False accordingly
        """
        for x in range(len(self._atom_row)):
            if row == self._atom_row[x-1]:
                if column == self._atom_column[x-1]:
                    self._atom_amount -= 1
                    return True
        self._atom_amount -= 1
        self._score -= 5
        return False

    def get_score(self):
        """
        Returns the current score
        """
        return self._score

    def atoms_left(self):
        """
        Returns the amount of atoms left to guess
        """
        return self._atom_amount


def main():
    print("working")
    game = BlackBoxGame([(7,6), (1, 7), (4, 6), (2,3)])
    #move_result = game.shoot_ray(3, 9)
    #print(move_result)
    #game.shoot_ray(0, 2)
    second_result = game.shoot_ray(1,0)
    print(second_result)
    guess_result = game.guess_atom(5, 5)
    score = game.get_score()
    atoms = game.atoms_left()


if __name__ == '__main__':
    main()

# first_hit(row/column traveled down, z list tells direction travelled (hit becomes z), x is where the run starts)

# shoot_shot(row, column, z (initialized), x is where the run starts)

# hit_something(row, col, hit(gives it the new direction))

# hit [what it hit, distance, direction]


# JUST ADDED RETURNS TO MY RUN METHODS
# Just work through finding each thing for the (3,9) shot