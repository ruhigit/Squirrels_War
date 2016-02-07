
import sys

# Check if square can be raided or sneaked
def check_square(my_player,board,players,curr_row,curr_col):

	#check for existing pieces horizontally and vertically

	#left horizontal
	if(curr_col-1>0):
		if(my_player==players[curr_row][curr_col-1]):
			temp_value_player,temp_value_opponent=raid(my_player,board,players,curr_row,curr_col)
			return temp_value_player,temp_value_opponent
	#right horizontal
	if(curr_col+1<4):
		if(my_player==players[curr_row][curr_col+1]):
			temp_value_player,temp_value_opponent=raid(my_player,board,players,curr_row,curr_col)
			return temp_value_player,temp_value_opponent

	#up vertical
	if(curr_row-1>0):
		if(my_player==players[curr_row-1][curr_col]):
			temp_value_player,temp_value_opponent=raid(my_player,board,players,curr_row,curr_col)
			return temp_value_player,temp_value_opponent

	#down vertical
	if(curr_row+1<4):
		if(my_player==players[curr_row+1][curr_col]):
			temp_value_player,temp_value_opponent=raid(my_player,board,players,curr_row,curr_col)
			return temp_value_player,temp_value_opponent

	#else Sneak
	temp_value_player=board[curr_row][curr_col]
	temp_value_opponent=0
	return temp_value_player,temp_value_opponent



def raid(my_player,board,players,curr_row,curr_col):

	if my_player=='X':
		opponent='O'
	else:
		opponent='X'

	temp_value_player=0;
	temp_value_opponent=0;

	#The new piece sum is added to player
	temp_value_player+=board[curr_row][curr_col]
	#any enemy pieces adjacent to the target square are turned to the players side.

	#left horizontal
	if(curr_col-1>0):
		if(opponent==players[curr_row][curr_col-1]):
			temp_value_player+=board[curr_row][curr_col-1]
			temp_value_opponent-=board[curr_row][curr_col-1]
			
	#right horizontal
	if(curr_col+1<4):
		if(opponent==players[curr_row][curr_col+1]):
			temp_value_player+=board[curr_row][curr_col+1]
			temp_value_opponent-=board[curr_row][curr_col+1]
			

	#up vertical
	if(curr_row-1>0):
		if(opponent==players[curr_row-1][curr_col]):
			temp_value_player+=board[curr_row-1][curr_col]
			temp_value_opponent-=board[curr_row-1][curr_col]
			

	#down vertical
	if(curr_row+1<4):
		if(opponent==players[curr_row+1][curr_col]):
			temp_value_player+=board[curr_row+1][curr_col]
			temp_value_opponent-=board[curr_row+1][curr_col]

	return (temp_value_player,temp_value_opponent)


def total_value(players,board):
	total_value_x=0;
	total_value_o=0;
	for row in range(0,4,1):

		for col in range(0,4,1):

			if(players[row][col]=='X'):
				total_value_x+=board[row][col]
			elif(players[row][col]=='O'):
				total_value_o+=board[row][col]

	return(total_value_x,total_value_o)


def tie_breaker(row1,col1,row2,col2):
	if row1<row2:
		return (row1,col1)
	elif row2<row1:
		return (row2,col2)
	elif col1<col2:
		return (row1,col1)
	else:
		return (row2,col2)

#E(s) = Total_Value_Player - Total_Value_Opponent
def GreedyBestfirstSearch(my_player,board,players):

	#total values of both players
	total_value_x,total_value_o=total_value(players,board)
	if my_player=='X':
		total_value_player=total_value_x
		total_value_opponent=total_value_o
	else:
		total_value_player=total_value_o
		total_value_opponent=total_value_x

	#evaluate each square
	max_value=0
	max_row=0
	max_col=0

	for row in range(0,4,1):

		for col in range(0,4,1):

			if(players[row][col]=='*'):
				temp_value_player,temp_value_opponent=check_square(my_player,board,players,row,col)
				curr_value=(total_value_player+temp_value_player)-(total_value_opponent+temp_value_opponent)

			if curr_value>max_value:
				max_value=curr_value
				max_row=row
				max_col=col

			elif curr_value == max_value:
				max_row,max_col=tie_breaker(row,col,max_row,max_col);

	return (max_row,max_col)

#decode the input file for part1
def decode_input_part1(inputFile):

	with open(inputFile,'r') as f:
		lines=f.readlines()
	
	# player
	my_player=lines[1].strip()

	# cut-off depth
	cut_off_depth=int(lines[2].strip())

	
	#create the 5 X 5 board
	board = [[0 for x in range(5)] for x in range(5)] 

	#board values

	board[0]=[int(x) for x in lines[3].split()]
	board[1]=[int(x) for x in lines[4].split()]
	board[2]=[int(x) for x in lines[5].split()]
	board[3]=[int(x) for x in lines[6].split()]
	board[4]=[int(x) for x in lines[7].split()]
	
	#create the 5 X 5 player grid
	players = [[0 for x in range(5)] for x in range(5)] 
	
	players[0]=list(lines[8].strip())
	players[1]=list(lines[9].strip())
	players[2]=list(lines[10].strip())
	players[3]=list(lines[11].strip())
	players[4]=list(lines[12].strip())

	return (my_player,cut_off_depth,board,players)
#decode the input file for part2
def decode_input_part2(inputFile):
	
	return

def main():
	
	
	#get the input file
	inputFile=sys.argv[2]

	#read the first line to determine which part
	with open(inputFile,'r') as f:
		task_number=f.readline()
	
	task_number=int(task_number)

	if task_number>0 and task_number<4: #part1
		my_player,cut_off_depth,board,players=decode_input_part1(inputFile);
		if task_number==1:
			next_row,next_col=GreedyBestfirstSearch(my_player,board,players)
			print(next_row,next_col)
	else:  #part2
		decode_input_part2(inputFile);
	

	return

if __name__=="__main__":
	main()