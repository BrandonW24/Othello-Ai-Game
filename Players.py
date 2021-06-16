'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
from OthelloBoard import *
import sys
from decimal import Decimal

pos_inf   = Decimal('Infinity')
neg_inf   = Decimal('-Infinity')

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
       
#My code starts here
#based off of the get move function just above this
#However this will get its move from the decision that minimax makes.
#the othelloboard.py file has great functions to utilize that are
#already there
#Get move should return the move that minimax has decided on the board
    def get_move(self, board):
        return self.minimax_choice(board)

#This is the minimax function, it has a champion variable that starts off holding the
#0th state of the list of successor moves, within the for loop we search for an action within
#the list of moves that have successor moves and then we call the play move function from
#OthelloBoard.py, it checks to see if the minimal value of our hypothetical move is valid
#if it is and we save that action as our champion action and return it. If not, we return
#champion as it was as we started.
    def minimax_choice(self, state: OthelloBoard):
        champion = list(state.has_successor_moves(self.symbol))[0]
        i = 0
        for action in list(state.has_successor_moves(self.symbol)):
            save_board = state.cloneOBoard()
            save_board.play_move(action[i], action[i+1], self.symbol)
            if(self.minimize_val(save_board) > float("-inf")):
                champion = action
        return champion
    
    #This is the utility function.
    #assign the found_value to the terminal state which is a positive value for a good outcome,
    # 0 for a neutral outcome, and a negative value for a bad outcome to avoid.
    #Checks the score of their symbol that they own against the opponents symbol.
    #THere are only three outcomes that can stem from this utility function.
    def util_function(self, state: OthelloBoard):
        if(state.count_score(self.symbol) > state.count_score(self.oppSym)):
            return 1
        elif (state.count_score(self.symbol) == state.count_score(self.oppSym)):
            return 0
        elif (state.count_score(self.symbol) < state.count_score(self.oppSym)):
            return -1

    #The state we are looking at here is the Othello Board
    #This function maximizes the player
    #The has_legal_moves_remaining function located within OthelloBoard.board
    #is very helpful here as it can deem how many moves are left for both X and O
    #This then checks to see if there are any moves remaining, if there are it goes through
    #The for-loop that has a list of legal moves that can be made by either symbol.
    #Towards the bottom this calls the built in MAX function to 
    #find the maximum value between the found_value node and the
    #self_minimize_val of the copied board.
    #We copy the state of the board here otherwise the minimax AI
    #will just inverse each action the user does.
    def maximize_val(self, state: OthelloBoard):
        num_legal_moves_x = state.has_legal_moves_remaining(self.symbol)
        num_legal_moves_o = state.has_legal_moves_remaining(self.oppSym)

        if(num_legal_moves_x == False): 
            if(num_legal_moves_o == False):
                return self.util_function(state)
        
        #This acts as an unbounded upper value for comparison sake
        #It's quite useful for finding the lowest value of something
        #for the initial found_value in the max function call. 
        #neg_inf is defined as = Decimal('-Infinity')
        
        found_value = neg_inf
        i = 0
        for action in list(state.has_successor_moves(self.symbol)):
            save_board = state.cloneOBoard()
            save_board.play_move(action[i], action[i+1], self.symbol)
            found_value = max(found_value, self.minimize_val(save_board))
            i = 0
        return found_value

    #Operates the same way as maximize_val however instead of
    #calling in the built in MAX function at the end it calls in the
    #min value between the the found_value node and the
    #self_maximize_val of the copied board.
    def minimize_val(self, state: OthelloBoard):
        num_legal_moves_x = state.has_legal_moves_remaining(self.symbol)
        num_legal_moves_o = state.has_legal_moves_remaining(self.oppSym)

        if(num_legal_moves_x == False): 
            if(num_legal_moves_o == False):
                return self.util_function(state)
        
        found_value = 1
        i = 0
        for action in list(state.has_successor_moves(self.oppSym)):
            save_board = state.cloneOBoard()
            save_board.play_move(action[i], action[i+1], self.oppSym)
            found_value = min(found_value, self.maximize_val(save_board))
            i = 0
        return found_value
