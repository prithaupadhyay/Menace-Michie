from collections import Counter
import random
import json

class Board:
    #constructor to make the board empty everytime
    def __init__(self):                          
        self.board=[' ',' ',' ',' ',' ',' ',' ',' ',' ']

    #to display the board positions and corresponding status
    def __str__(self):                   
        return("\n 0 || 1 || 2 \t %s || %s || %s \n 3 || 4 || 5\t %s || %s || %s \n 6 || 7 || 8\t %s || %s || %s " % (self.board[0], self.board[1], self.board[2], self.board[3], self.board[4], self.board[5], self.board[6], self.board[7], self.board[8]))

    #to check if the entered move is valid or not
    def validMoves(self,move):              
        try:                                #typecast the entered move as an integer 
            move=int(move)
        except ValueError:
            return False

    #check if the entered move is empty or not
        if 0<=move<=8 and self.board[move]==" ":       
            return True
        return False

     # to get the winCondition condition
    def winCondition(self):                         
         #3 cases when 0 is non-empty, when 4 is non-empty or when 8 is non-empty
        return ((self.board[0] != ' ' and            
                 ((self.board[0] == self.board[1] == self.board[2]) or
                  (self.board[0] == self.board[3] == self.board[6]) or
                  (self.board[0] == self.board[4] == self.board[8])))
                or (self.board[4] != ' ' and
                    ((self.board[1] == self.board[4] == self.board[7]) or
                    (self.board[3] == self.board[4] == self.board[5]) or
                    (self.board[2] == self.board[4] == self.board[6])))
                or (self.board[8] != ' ' and
                    ((self.board[2] == self.board[5] == self.board[8]) or
                    (self.board[6] == self.board[7] == self.board[8]))))    

    #to get the draw condition when all the 9 blocks are filled, ie:non-empty
    def drawCondition(self):                             
        return all((x!=" " for x in self.board))


    # to place the marker on selected position
    def playMove(self,position, marker):        
        self.board[position]=marker

    #to append all the played positions in the board, keeps the board updated after every move
    def boardString(self):                          
        return ''.join(self.board)

    
class Menace:
    def __init__(self):
        #empty dictionary of matchboxes to store states during the games
        self.matchBoxes = {}      
        #initializing the number of wins, loses and draws of menace
        self.numWin=0
        self.numLose=0
        self.numDraw=0
    
    #initialising the list of all the moves played by menace
    def startGame(self):
        self.movesPlayed=[]

     #to get the possible moves to be played by menace
    #we need to check if the current state of the board is present in the matchboxes dictionary or not, else we'll add that state in the matchbox dictionary

    def getMove(self, board):       
        #to get the current state of the board from the board string function and store it in the board variable      
        board=board.boardString()      

        if board not in self.matchBoxes:
            #new beads denotes the possible positions to play
            newBeads=[pos for pos,mark in enumerate(board) if mark==" "] 
            #suppose red color denotes 4th position, if 4th is empty then it will be present in new beads. Now, we want proper selection, we'll amplify the number of possible play move. ie: increase the number of red beads in that particular matchbox.
            self.matchBoxes[board]=newBeads * ((len(newBeads)+2)//2)

        beads=self.matchBoxes[board]

        #if  there are beads in the matchbox, ie: when no move is preferred in that state.
        #we gave punishment for every mistake and if it continues, it will turn to 0
        if len(beads):
            bead=random.choice(beads)
            self.movesPlayed.append((board,bead))      
        else:
            bead=-1
        return bead

    #if this state gives positive result, add 3 more beads of same
    def ifWin(self):
        for (board,bead) in self.movesPlayed:
            self.matchBoxes[board].extend([bead,bead,bead])
        self.numWin+=1

    #if this function results true, we just append one bead
    def ifDraw(self):
        for (board,bead) in self.movesPlayed:
            self.matchBoxes[board].append(bead)
        self.numDraw+=1
    
    #if this function returns true, we delete the bead
    def ifLose(self):
        for (board,bead) in self.movesPlayed:
            matchbox=self.matchBoxes[board]
            del matchbox[matchbox.index(bead)]
        self.numLose+=1
        
    #to count the number of states stored
    def length(self):
        return (len(self.matchBoxes))

    
class Human:
    def __init__(self):
        pass

    def startGame(self):
        print("Get Ready!!")

    #take the move from user
    def getMove(self, board):
        while True:
            move=input("make move ")
            if board.validMoves(move):
                break
            print("not a valid move")
            
        return int(move)

    #to print the results of the games
    def ifWin(self):
        print("Human Won")
        
    def ifDraw(self):
        print("You and me are equal. Its a draw")
        
    def ifLose(self):
        print("Human Lost the game")
        

#function to play game
def playGame(first, second, silent=False):
    first.startGame()
    second.startGame()
    board=Board()

    if not silent:
        print("\nStarting a new game")
        print(board)
    
    while True:
        move=first.getMove(board)
        if move==-1:
            if not silent:
                print("Player Resigned")
            first.ifLose()
            second.ifWin()
            break
        
        board.playMove(move,'X')

        if not silent:
            print(board)
        if board.winCondition():
            first.ifWin()
            second.ifLose()
            break
        if board.drawCondition():
            first.ifDraw()
            second.ifDraw()
            break


        move=second.getMove(board)

        if move==-1:
            if not silent:
                print("Player Resigned")
            second.ifLose()
            first.ifWin()
            break
        
        board.playMove(move,'O')

        if not silent:
            print(board)
        if board.winCondition():
            second.ifWin()
            first.ifLose()
            break


    
if __name__=='__main__':
    menaceFirst=Menace()
    menaceSecond=Menace()
    human=Human()

    print("Input 1 for continuing with the trained model otherwise press 0")
    n = int(input())

    #if the user selected not to use trained model, then train it for 100000 matches
    if n==0:
        for i in range(100000):
            playGame(menaceFirst,menaceSecond,silent=True)
     
        state1 = menaceFirst.length()
        state2 = menaceSecond.length()
        
        if state1>=state2:
            print("Number of states ",state1)
            with open('states.json', 'w') as f:
                json.dump(menaceFirst.matchBoxes, f, sort_keys=False, indent=4)

        else:
            print("Number of states ",state2)
            with open('states.json', 'w') as f:
                json.dump(menaceSecond.matchBoxes, f, sort_keys=False, indent=4)

        playGame(menaceFirst,human)

    #if the user selects to use the trained model, fetch it from the json file
    elif n==1:
        menaceTrained = Menace()
        with open('states.json', 'r') as f:
            menaceTrained.matchBoxes = json.load(f)
        print("Number of states ",menaceTrained.length())
        playGame(menaceTrained,human)


    
