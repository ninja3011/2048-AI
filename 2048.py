#2048 Game, GUI Interface and in future AI implementations
#Created by Ninad jangle (ninja3011)
#2:23pm 23/08/2020
#Every alpghabet handtyped. Zero Copy pasting.
#Following the work done by kiteco

#Tkinter provides classes which allow the display, positioning and control of widgets.
import tkinter as tk 
#Random variable generators.
import random
#colors.py is a userdefined python file for holding the colors needed for files and the GUI
import colors as c

#Frame widget which may contain other widgets and can have a 3D border.
class Game(tk.Frame): 
    def __init__(self):
        #Construct a frame widget with the parent MASTER.
        tk.Frame.__init__(self)
        #Position a widget in the parent widget in a grid
        #grid(​padx, pady, row, sticky, column)
        self.grid()
        self.master.title('2048')
        self.main_grid = tk.Frame(
            self,
            bg=c.GRID_COLOR,
            bd=3,
            width=400, 
            height=400
            )
        self.main_grid.grid(pady=((80,0)))
        self.make_GUI()
        self.start_game()

        self.master.bind('<Left>',self.left)
        self.master.bind('<Right>',self.right)
        self.master.bind('<Up>',self.up)
        self.master.bind('<Down>',self.down)

        #Call the mainloop of Tk.
        self.mainloop()

    def make_GUI(self):
        #make grid
        self.cells=[]
        for i in range(4):
            row = []
            for j in range(4):
                cell_frame=tk.Frame(
                    self.main_grid,
                    bg=c.EMPTY_CELL_COLOR,
                    width=100,
                    height=100
                    )
                cell_frame.grid(row=i,column=j,padx=5, pady=5)
                cell_number=tk.Label(self.main_grid,bg=c.EMPTY_CELL_COLOR)
                cell_number.grid(row=i, column=j)
                cell_data ={'frame': cell_frame, 'number': cell_number}
                #Override to enforce validation.
                row.append(cell_data)
            self.cells.append(row)

        #making the score header
        score_frame = tk.Frame(self)
        score_frame.place(relx=0.5,y=40,anchor='center')
        #Label widget which can display text and bitmaps
        tk.Label(
            score_frame,
            text='Score',
            font=c.SCORE_LABEL_FONT).grid(row=0)
        self.score_label=tk.Label(score_frame,text='0', font=c.SCORE_FONT)
        self.score_label.grid(row=1)

    def start_game(self):
        #creating a matrix of zeroes
        #matrix: A list subclass for Python 2 that behaves like Python 3's list.
        self.matrix=[[0] * 4 for _ in range(4)]
        #fill 2 random cells with 2s
        #randint(): Return random integer in range [a, b], including both end points
        row = random.randint(0,3)
        col = random.randint(0,3)
        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text='2')

        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)

        self.matrix[row][col] = 2
        self.cells[row][col]['frame'].configure(bg=c.CELL_COLORS[2])
        self.cells[row][col]['number'].configure(
            bg=c.CELL_COLORS[2],
            fg=c.CELL_NUMBER_COLORS[2],
            font=c.CELL_NUMBER_FONTS[2],
            text= '2')

        self.score=0

# Creating the Matrix Manipulation functions
# Different successions of these functions will 
#simulate the L,R,U,D arrow button pushes
    
    def stack(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            fill_position = 0
            for j in range(4):
                if(self.matrix[i][j] != 0):
                    new_matrix[i][fill_position]=self.matrix[i][j]
                    fill_position+=1
        self.matrix=new_matrix

    def combine(self):
        for i in range(4):
            for j in range(3):
                if(self.matrix[i][j] != 0 and self.matrix[i][j] == self.matrix[i][j+1]):
                    self.matrix[i][j] *= 2
                    self.matrix[i][j+1] = 0
                    self.score += self.matrix[i][j]
        
    def reverse(self):
        new_matrix= []
        for i in range(4):
            new_matrix.append([])
            for j in range(4):
                new_matrix[i].append(self.matrix[i][3-j])
        self.matrix=new_matrix

    def transpose(self):
        new_matrix = [[0] * 4 for _ in range(4)]
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = self.matrix[j][i]
        self.matrix=new_matrix

    def add_new_tile(self):
        row=random.randint(0,3)
        col=random.randint(0,3)
        while(self.matrix[row][col] != 0):
            row = random.randint(0,3)
            col = random.randint(0,3)
        #random.choice([...]): Chooses a random element from a non-empty sequence.
        self.matrix[row][col]= random.choice([2,4])

        #Updating the GUI to match the current Matrix

    def update_GUI(self):
        for i in range(4):
            for j in range(4):
                cell_value = self.matrix[i][j]
                if( cell_value ==0):
                    self.cells[i][j]['frame'].configure(bg=c.EMPTY_CELL_COLOR)
                    self.cells[i][j]['number'].configure(
                        bg=c.EMPTY_CELL_COLOR,
                        text='')
                else:
                    self.cells[i][j]['frame'].configure(
                        bg=c.CELL_COLORS[cell_value])
                    self.cells[i][j]['number'].configure(
                        bg=c.CELL_COLORS[cell_value],
                        fg=c.CELL_NUMBER_COLORS[cell_value],
                        font=c.CELL_NUMBER_FONTS[cell_value],
                        text=str(cell_value)
                        )
        self.score_label.configure(text=self.score)
        self.update_idletasks()


    def left(self,event):
        self.stack()
        self.combine()
        self.stack()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def right(self, event):
        self.reverse()
        self.stack()
        self.combine()
        self.stack()
        self.reverse()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def up(self, event):
        self.transpose()
        self.stack()
        self.combine()
        self.stack()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

    def down(self, event):
        self.transpose()
        self.reverse()
        self.stack()
        self.combine()
        self.stack() 
        self.reverse()
        self.transpose()
        self.add_new_tile()
        self.update_GUI()
        self.game_over()

        #check if any moves are possible

    def horizontal_move_exists(self):
        for i in range(4):
            for j in range(3):
                if(self.matrix[i][j] == self.matrix[i][j+1]):
                    return True
        return False

    def vertical_move_exists(self):
        for i in range(3):
            for j in range(4):
                if self.matrix[i][j] == self.matrix[i + 1][j]:
                    return True
        return False

    def game_over(self):
        if any(2048 in row for row in self.matrix):
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5,rely=0.5,anchor='center')
            tk.Label(
                game_over_frame,
                text='You win!',
                bg=c.WINNER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font=c.GAME_OVER_FONT).pack()
        elif not any(0 in row for row in self.matrix) and not self.horizontal_move_exists() and not self.vertical_move_exists():
            game_over_frame = tk.Frame(self.main_grid, borderwidth=2)
            game_over_frame.place(relx=0.5, rely=0.5,anchor='center')
            tk.Label(
                game_over_frame,
                text='Game Over!',
                bg=c.LOSER_BG,
                fg=c.GAME_OVER_FONT_COLOR,
                font= c.GAME_OVER_FONT)

def main():
    Game()

if __name__=='__main__':
    main()















