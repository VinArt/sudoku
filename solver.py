import numpy as np
import time

class Solver:
    def __init__(self):
        self.probabilities = np.zeros((9, 9, 9))
        self.processed = np.zeros((9, 9))
        self.counter = 0
        
    def load_board(self, filename):
        self.board = np.genfromtxt(filename, delimiter=",", dtype=int)
        for i in range(9):
            for j in range(9):
                if self.board[i, j] != 0:
                    self.processed[i, j] = True
                
    def load_solution(self, filename):
        self.solution = np.genfromtxt(filename, delimiter=",", dtype=int)
                
    def get_block(self, hblock, vblock):
        hblock = int(np.floor(hblock/3))
        vblock = int(np.floor(vblock/3))
        if(vblock > 2 or hblock > 2 or vblock < 0 or hblock < 0):
            return -1
        return self.board[3*hblock:3 + 3*hblock, 3*vblock:3 + 3*vblock]
            
    def get_row(self, row_num):
        return self.board[row_num:row_num+1][0]
    
    def get_column(self, column_num):
        return self.board[:, column_num:column_num+1].T[0]
    
    def compare_with_solution(self):
        return np.all(np.equal(self.board, self.solution))
    
    def update_probability(self, x, y):
        if self.processed[y, x] == 1:
            return
        self.counter += 1
        row = self.get_row(y)
        #print("for x:", x, " y:", y)
        #print("row:", row)
        existing_numbers = np.array([])
        for number in row:
            if number != 0:
                existing_numbers = np.append(existing_numbers, number)
                self.probabilities[y, x, number - 1] = 0
        column = self.get_column(x)
        #print("column:", column)
        for number in column:
            if number != 0:
                existing_numbers = np.append(existing_numbers, number)
                self.probabilities[y, x, number - 1] = 0
        block = self.get_block(y, x)
        #print("block:\n", block)
        for number in block.reshape((1,9))[0]:
            if number != 0:
                existing_numbers = np.append(existing_numbers, number)
                self.probabilities[y, x, number - 1] = 0
        existing_numbers = np.asarray(np.unique(existing_numbers), dtype=int)
        #print("existing numbers:", existing_numbers)
        for number in range(1, 10):
            if number not in existing_numbers:
                probability = 1 / (9 - existing_numbers.size)
                #print("number", number, " has probability", probability)
                self.probabilities[y, x, number - 1] = probability
                if probability == 1:
                    self.board[y, x] = number
                    self.processed[y, x] = True
                    
    def compute_index(self):
        print(self.probabilities[:,:,:])
        
    def update_probabilities(self):
        for i in range(9):
            for j in range(9):
                self.update_probability(j, i)
        self.compute_index()
        if 1 not in self.probabilities:
            print("Cannot solve in one pass, max probability: ", np.max(self.probabilities))
            exit(0)
    
if __name__ == "__main__":
    s = Solver()
    s.load_board("board3")
    s.load_solution("solution")
    np.set_printoptions(precision=2, suppress=True)
    ts_start = time.time()
    while (not np.all(s.processed)):
        s.update_probabilities()
        
    ts_end = time.time()
    print("done: ", ts_end - ts_start)
    '''
    board = np.copy(s.board)
    processed = np.copy(s.processed)
    ts_start = time.time()
    for i in range(1000):
        while (not np.all(s.processed)):
            s.update_probabilities()
        s.processed = np.copy(processed)
        s.board = np.copy(board)
        s.counter = 0
        #print(np.all(np.equal(s.board, s.solution)))
        #print(s.counter)
    ts_end = time.time()
    print("done: ", ts_end - ts_start)
    '''
