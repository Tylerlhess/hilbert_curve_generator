###################################################################################################################
#    Copyright 2020 Tyler Hess
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#
#    Hilbert curve generator
#
#    Hilbert curves are constructed deterministically from a combinations of 4 patterns.
#    To simplify my life I enumerated them 1 through 4 based on order of appearance in the pattern.
#    Assuming we are starting at (0,0) and traversing positions in an image the patterns are as follows
#    1. down -> right -> up
#    2. right -> down -> left
#    3. up -> left -> down
#    4. left -> up -> right
#
#    Further the start of every block of 4 determines the 4 patterns in that block
#    As one block is completed it is then used as the starter block for the next 3 blocks of its size.


def hilbert_curve(start_point=(0, 0), step_size=1):
    """Generator function that returns hilbert curve coordinates infinitely"""
    position = start_point
    _shape = shapes_gen()
    shape = next(_shape) # setup shape 0 so it starts correctly. else it starts with 1,1 and is off in the rest of the calculations.
    while True:
        for movement in move(shape, step_size):
            position = cmb(position, movement)
            yield position
        previous_shape = shape
        shape = next(_shape)
        position = cmb(position, next_start(previous_shape, shape, step_size))


def four_from_one_gen(shape):
    """Finite generator to determine the three final block shapes given the first shape."""
    s = {1: [1, 2, 2, 3],
         2: [2, 1, 1, 4],
         3: [3, 4, 4, 1],
         4: [4, 3, 3, 2]}
    for y in s[shape]:
        yield y


def shapes_gen():
    """Infinite Generator of the next pattern"""
    lists = []
    position = 0
    # have to start the first block manually.
    for x in four_from_one_gen(1):
        # appending the blocks to a list as once the block is complete it becomes the seed for the next block
        lists.append(x)
        yield x
    position += 1
    # Now that the seed block is created we can keep expanding with the position in the list as a guide.
    # Note the list grows at O^4 but there is no easy way to get these two things independently
    while True:
        for x in four_from_one_gen(lists[position]):
            lists.append(x)
            yield x
        position += 1


def next_start(previous_shape, next_shape, step_size):
    """Function to get the position translation for the next block"""
    grid = {0: {1: (0, 0), 2: (0, 0), 3: (0, 0), 4: (0, 0)},
            1: {1: (0, 1), 2: (0, 1), 3: (-1, 0), 4: (-1, 0)},
            2: {1: (1, 0), 2: (1, 0), 3: (0, -1), 4: (0, -1)},
            3: {1: (1, 0), 2: (1, 0), 3: (0, -1), 4: (0, -1)},
            4: {1: (0, 1), 2: (0, 1), 3: (-1, 0), 4: (-1, 0)}}
    return calc_step(grid[previous_shape][next_shape], step_size)


def move(shape, step_size):
    """Finite generator to get the translation coordinates for each block type"""
    moves = {0: [(0, 0)],
             1: [(0, 0), (1, 0), (0, 1), (-1,  0)],
             2: [(0, 0), (0, 1), (1, 0), (0, -1)],
             3: [(0, 0), (-1, 0), (0, -1), (1,  0)],
             4: [(0, 0), (0, -1), (-1, 0), (0, 1)]}
    for a in moves[shape]:
        yield calc_step(a, step_size)


def cmb(start, translation):
    """Function to simplify position translation returning the new position"""
    return (start[0] + translation[0], start[1] + translation[1])

def calc_step(point, step):
    return (point[0]*step, point[1]*step)

if __name__ == "__main__":
    x = 0
    q = hilbert_curve()
    while x < 1700:
       print(next(q), x)
       x+=1

