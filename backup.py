
import sys

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

	for row in range(0,5,1):
		for col in range(0,5,1):

			if(players[row][col]=='*'):
				temp_value_player,temp_value_opponent=check_square(my_player,board,players,row,col)
				#E(s) = Total_Value_Player - Total_Value_Opponent
				curr_value=(total_value_player+temp_value_player)-(total_value_opponent+temp_value_opponent)

			if curr_value>max_value:
				max_value=curr_value
				max_row=row
				max_col=col

			elif curr_value == max_value:
				max_row,max_col=tie_breaker(row,col,max_row,max_col);

	return (max_row,max_col)

def print_in_file(curr_row,curr_col,depth,bestValue,op_file):
	if curr_row==-1 and curr_col==-1:
		name="root"
	else:
		name=chr(curr_col+97).upper()+str(curr_row+1)

	_infinity=float("-inf")
	infinity=float("inf")
	if bestValue == _infinity:
		bestValueChar="-Infinity"
	elif bestValue ==infinity:
		bestValueChar="Infinity"
	else:
		bestValueChar=str(bestValue)
	op_file.write(name+","+str(depth)+","+bestValueChar)
	op_file.write("\n")
	return

def minimaxalgo(op_file,curr_row,curr_col,depth,cut_off_depth,maximizingPlayer,my_player,my_opponent,board,players,total_value_player,total_value_opponent):

	#if depth is 0 or node is a terminal node
	
	if depth==cut_off_depth:

		bestValue=(total_value_player)-(total_value_opponent)
		print_in_file(curr_row,curr_col,depth,bestValue,op_file)
		return bestValue

	#MAX
	if maximizingPlayer:
		bestValue=float("-inf")
		# for each child of the node, that is each unoccupied square
		for row in range(0,5,1):
			for col in range(0,5,1):
				if(players[row][col]=='*' and (row!=curr_row or col!=curr_col)):
					players[row][col]=my_player
					#call for child nodes
					print_in_file(curr_row,curr_col,depth,bestValue,op_file)
					temp_value_player,temp_value_opponent=check_square(my_player,board,players,row,col)
					value=minimaxalgo(op_file,row,col,depth+1,cut_off_depth,0,my_player,my_opponent,board,players,total_value_player+temp_value_player,total_value_opponent+temp_value_opponent)
					players[row][col]='*'
					#print if not leaf node
					if(depth+1!=cut_off_depth):
						print_in_file(row,col,depth+1,value,op_file)
					if value>bestValue:
						bestValue=value
						max_row=row
						max_col=col
					elif value == bestValue:
						max_row,max_col=tie_breaker(row,col,max_row,max_col)
		return (bestValue)

	#MIN	
	else:
		bestValue=float("inf")
		for row in range(0,5,1):
			for col in range(0,5,1):
				#for each child
				if(players[row][col]=='*' and (row!=curr_row or col!=curr_col)):
					players[row][col]=my_opponent
					#call for child nodes
					# ------------------ print --------------------------------
					print_in_file(curr_row,curr_col,depth,bestValue,op_file)
					temp_value_opponent,temp_value_player=check_square(my_opponent,board,players,row,col)
					value=minimaxalgo(op_file,row,col,depth+1,cut_off_depth,1,my_player,my_opponent,board,players,total_value_player+temp_value_player,total_value_opponent+temp_value_opponent)
					players[row][col]='*'
					#print if not leaf node
					if(depth+1!=cut_off_depth):
						print_in_file(row,col,depth+1,value,op_file)
					if value<bestValue:
						bestValue=value
						max_row=row
						max_col=col
					elif value == bestValue:
						max_row,max_col=tie_breaker(row,col,max_row,max_col)
					
		return bestValue




def minimax(my_player,cut_off_depth,board,players):

	op_file=open('traverse_log.txt', 'w')
	op_file.write("Node,Depth,Value\n")
	#total values of both players
	total_value_x,total_value_o=total_value(players,board)
	if my_player=='X':
		total_value_player=total_value_x
		total_value_opponent=total_value_o
		my_opponent='O'
	else:
		total_value_player=total_value_o
		total_value_opponent=total_value_x
		my_opponent='X'

	bestValue=float("-inf")
	maximizingPlayer=1
	row=-1
	col=-1
	max_row=1
	max_col=1
	bestValue=minimaxalgo(op_file,row,col,0,cut_off_depth,maximizingPlayer,my_player,my_opponent,board,players,total_value_player,total_value_opponent)
	op_file.write("root,0,"+str(bestValue))
	op_file.close()
	return(max_row,max_col)

def alpha_beta_pruning(my_player,cut_off_depth,board,players):
	return

# Check if square can be raided or sneaked
def check_square(my_player,board,players,curr_row,curr_col):

	#check for existing pieces horizontally and vertically

	#left horizontal
	if(curr_col-1>=0):
		if(my_player==players[curr_row][curr_col-1]):
			temp_value_player,temp_value_opponent=raid(my_player,board,players,curr_row,curr_col)
			return temp_value_player,temp_value_opponent
	#right horizontal
	if(curr_col+1<=4):
		if(my_player==players[curr_row][curr_col+1]):
			temp_value_player,temp_value_opponent=raid(my_player,board,players,curr_row,curr_col)
			return temp_value_player,temp_value_opponent

	#up vertical
	if(curr_row-1>=0):
		if(my_player==players[curr_row-1][curr_col]):
			temp_value_player,temp_value_opponent=raid(my_player,board,players,curr_row,curr_col)
			return temp_value_player,temp_value_opponent

	#down vertical
	if(curr_row+1<=4):
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
	if(curr_col-1>=0):
		if(opponent==players[curr_row][curr_col-1]):
			temp_value_player+=board[curr_row][curr_col-1]
			temp_value_opponent-=board[curr_row][curr_col-1]
			
	#right horizontal
	if(curr_col+1<=4):
		if(opponent==players[curr_row][curr_col+1]):
			temp_value_player+=board[curr_row][curr_col+1]
			temp_value_opponent-=board[curr_row][curr_col+1]
			

	#up vertical
	if(curr_row-1>=0):
		if(opponent==players[curr_row-1][curr_col]):
			temp_value_player+=board[curr_row-1][curr_col]
			temp_value_opponent-=board[curr_row-1][curr_col]
			

	#down vertical
	if(curr_row+1<=4):
		if(opponent==players[curr_row+1][curr_col]):
			temp_value_player+=board[curr_row+1][curr_col]
			temp_value_opponent-=board[curr_row+1][curr_col]

	return (temp_value_player,temp_value_opponent)


def total_value(players,board):
	total_value_x=0;
	total_value_o=0;
	for row in range(0,5,1):

		for col in range(0,5,1):

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
			players[next_row][next_col]=my_player
		elif task_number==2:
			next_row,next_col=minimax(my_player,cut_off_depth,board,players)
			players[next_row][next_col]=my_player
		elif task_number==3:
			next_row,next_col=alpha_beta_pruning(my_player,cut_off_depth,board,players)
			players[next_row][next_col]=my_player
	else:  #part2
		decode_input_part2(inputFile);
	

	#create output file
	with open('next_state.txt', 'w') as op_file:
		for row in range(0,5,1):
			for col in range(0,5,1):
				op_file.write(players[row][col])
			op_file.write("\n")
	return

if __name__=="__main__":
	main()