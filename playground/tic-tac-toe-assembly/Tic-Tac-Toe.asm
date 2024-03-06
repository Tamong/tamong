###---TO BEGIN---################################################################################
# Philip Wallis 										#
# This project was completed solely by P. Wallis with online resources, no copy/pasted code.	#
# To run the program, open this file in MARS 4.5 by Missouri State University.			#
# Assemble the file by pressing F3, then run the program by pressing F5.			#
# To play the game, type a number between 0-8 and hit enter when prompted to make a move.	#
# To replay the game, reassemble and run the program again.					#
#################################################################################################


###---DATA---####################################################################################################################################
# The data segment holds the initial values of the board which is modified by the player or the computer move procedure.			#
# The board is also used to check to see if there is a winner in the game.									#
# instruction1 and instruction2 is called in the beginning of the play procedure to display the instructions.					#
# space, bar, and divider is used to display the board in draw_board procedure.									#
# input, invalid, computerMove is used to show the player what to do or show what happened, and 'X' and 'O' are used to replace the move.	#
# winText, loseText, tieText is used to display who won, after determining the winner of the game.						#
#################################################################################################################################################
.data					#data segment

	board:		.word '0', '1', '2', '3', '4', '5', '6', '7', '8'
	
	instruction1: 	.asciiz "\n\nWelcome to Tic Tac Toe!\nYou will be X and the computer will be O.\n"
	instruction2:	.asciiz "Play by typing a number from 0 to 8 to place your move on the corresponsding spot on the board!\n\n"
	space:		.asciiz " "
	bar: 		.asciiz " | "
	divider: 	.asciiz "\n---+---+---\n"
	
	input: 		.asciiz "\nPlayer, enter your move: "
	invalid:	.asciiz "Error! Invalid move! Try again.\n"
	computerMove:	.asciiz "\nComputer placed its move.\n"
	user:		.word 'X'
	computer:	.word 'O'

	winText: 	.asciiz "\nPlayer wins!!\n"
	loseText:	.asciiz "\nPlayer Lost!! Computer Wins.\n"
	tieText: 	.asciiz "\nTie game!! No one won.\n"

	.align 4


.text					# Code segment
.globl	main				# declare main to be global

###---MAIN---############################################################################################################
# This main procedure is the one that initializes everything. 								#
# It initializes $s0 = board, $t1 = 'X' and $t2 = 'O' and $t7 = 4 to represent individual element size in board.	#
# It calls play procedure which is the actual game, then exits in case of an error.					#
#########################################################################################################################
main:
	
	# Initialize the board, $s0 holds the board data
	li      $v0, 0
    	la      $s0, board		# $s0 holds board
    	
	lw $t1, user			# $t1 holds X
	lw $t2, computer		# $t2 holds O
	li $t7, 4 			# holds 4 for byte movements
	
	j play
	j exit				# in case of error

###---PLAY---####################################################################################################
# The play function starts by printing the instructions to the user.						#
# It plays 4 set of move, and each set contains draw_board, a player_move, then a computer_move.		#
# Then another player_move is called in case the game hasn't ended by then to place the 9th move.		#
# If no winner is determined by the end of the 9th move, it calls the tied procedure and ends the program.	#
#################################################################################################################
play:
	# Print instructions
	la $a0, instruction1
	li $v0, 4
	syscall

	la $a0, instruction2
	li $v0, 4
	syscall
	
	# 4 set of moves
	 
	jal draw_board
	jal player_move
	jal computer_move
	 
	jal draw_board
	jal player_move
	jal computer_move
	 
	jal draw_board
	jal player_move
	jal computer_move
	 
	jal draw_board
	jal player_move
	jal computer_move
	 
	# last move from the user
	jal draw_board
	jal player_move
	 
	# if no winner is determined by the end of the program
	jal tied
	 	 
	jal exit
###---PLAYER_MOVE---#############################################################################
# It calls the player_place, then calls check_winner to determine the winner.			#
# If there is no winner after calling, it will return to play procedure to continue the game.	#
#################################################################################################
player_move:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	jal player_place
	
	jal check_winner 		# check if someone has won
	
	lw $ra, 4($sp)
	add $sp, $sp, 4	
	jr $ra
###---PLAYER_PLACE---############################################################################################################################
# It prompts the user to enter a number. Then it reads the user input and saves the input number to $t0.					#
# Then it is multiplied by $t7, or 4, to determine the place on the board, and calls invalid_move to check for invalid input.			#
# If the invalid move has no errors, it returns to the procedure to replace the place on board with an 'X', then returns to player_move.	#
#################################################################################################################################################
player_place:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	# Print instructions
	la $a0, input
	li $v0, 4
	syscall
	
	# input
	li $v0, 5
    	syscall

    	# Moving the integer input to another register
    	move $t0, $v0
    
	# save input
	mult  $t0, $t7 			# 4 times input
	mfhi $s1 
	mflo $s2 			# holds actual value for 4*input
	lw  $t5, board($s2) 		# holds 0~8 or 'X' or 'O'
	
	jal invalid_move 		# check if its valid 
	
	#replace the value of item in board to X in $t1
	la $t5, board($s2)
	sw $t1, 0($t5)

	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra

###---INVALID_MOVE && PRINT_INVALID---###################################################
# It will get the player input location, and check if it is occupied by an 'X' or 'O'.	#
# If it is occupied, it will call print_invalid procedure.				#
# In the invalid procedure, it will display that it is invalid and call draw_board.	#
# It calls player_place again if it reaches here, and will re-prompt everything again.	#
# If it executes without invalid moves, it will return back to player_move.		#
#########################################################################################
invalid_move:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	beq $t5, $t1, print_invalid 	# if board($s2) holds 'X'
	beq $t5, $t2, print_invalid 	# if board($s2) holds 'O'
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra

print_invalid:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	# print invalid input text
	la $a0, invalid
	li $v0, 4
	syscall
	
	jal draw_board 			# draw board again
	jal player_place 		# go back to user input
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
###---COMPUTER_MOVE && COMPUTER_PLACE && COMPUTER PLACED---##############################################
# Similar to player_move, but this calls a computer_placed to display that computer has made its move.	#
# computer_place also acts similar to player_place, but instead of getting an input from the user,	#
# it will generate a random number between 0-8 and call the invalid_computer to verify the input.	#
# If the generated move is valid, it will place an 'O'on the board.					#
#########################################################################################################
computer_move:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	jal computer_place
	jal computer_placed
	
	jal check_winner 		# check if someone has won
	
	lw $ra, 4($sp)
	add $sp, $sp, 4	
	jr $ra
	
computer_place:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	# Generate random number between 0-8
	li $v0, 42 			# 42 is for random number
	li $a1, 9   			# set upper bound
	syscall     			# your generated number will be at $a0

	move $s3, $a0			# store in $s3
	    	
    	# save computer input
	mult  $s3, $t7 			# 4 times input
	mfhi $s4 
	mflo $s5 			# holds actual value for 4*input
	lw  $t6, board($s5) 		# holds 0~8 or 'X' or 'O'
	
	jal invalid_computer 		# check if its valid 
	
	#replace the value of item in board to O in $t2
	la $t6, board($s5)
	sw $t2, 0($t6)
    	
    	
	lw $ra, 4($sp)
	add $sp, $sp, 4	
	jr $ra
	
computer_placed:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
    	la $a0, computerMove		# print that the computer has placed
	li $v0, 4
	syscall
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
###---INVALID_COMPUTER && COMPUTER_RETRY---######################################################################
# invalid_computer acts like invalid_move and compares the computer move to any existing board elements.	#
# computer_retry is also just like print_invalid, it calls the computer_place function again to repeat.		#
#################################################################################################################
invalid_computer:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	
	beq $t6, $t1, computer_retry 	# if board($s2) holds 'X'
	beq $t6, $t2, computer_retry 	# if board($s2) holds 'O'
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
computer_retry:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	jal computer_place		# recall the computer_move to replay the move
    	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
###---CHECK_WINNER && CHECK_$$$---###############################################################################
# check_winner calls check_$$1 which is the first two numbers of the list of three.				#
# the first $ represents: r = row, c = column, d = diagonal.							#
# The second $ represents 1 = first, 2 = second, 3 = third, options for the specific direction of winning.	#
# In check_$$1, it will compare the first two numbers of the winning three then if those two match in value,	#
# it will call check_$$2, which will compare the second and third values. 					#
# If the check_$$2 beq gives a true output, then it will go to WINNER_FOUND.					#
# If there is no match at any point, it will skip the next step, and go check the next set of winning three.	#
#################################################################################################################
check_winner:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	jal check_r11 # 0, 1, 2
	jal check_r21 # 3, 4, 5
	jal check_r31 # 6, 7, 8
	jal check_c11 # 0, 3, 6
	jal check_c21 # 1, 4, 7
	jal check_c31 # 2, 5, 8
	jal check_d11 # 0, 4, 8
	jal check_d21 # 2, 4, 6
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
#####################################
# Rows
check_r11:
	# 0, 1, 2
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	lw $t5, 0($s0)
	lw $t6, 4($s0)
	beq $t5, $t6, check_r12		# compare 0, 1, goto check r1
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
check_r21:
	# 3, 4, 5
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	lw $t5, 12($s0)
	lw $t6, 16($s0)
	beq $t5, $t6, check_r22		# compare 3, 4, goto check r2
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
check_r31:
	# 6, 7, 8
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	lw $t5, 24($s0)
	lw $t6, 28($s0)
	beq $t5, $t6, check_r32		# compare 6, 7, goto check r3
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
# Columns
check_c11:
	# 0, 3, 6
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	lw $t5, 0($s0)
	lw $t6, 12($s0)
	beq $t5, $t6, check_c12		# compare 0, 3, goto check c1
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
check_c21:
	# 1, 4, 7
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	lw $t5, 4($s0)
	lw $t6, 16($s0)
	beq $t5, $t6, check_c22		# compare 1, 4, goto check c2
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
check_c31:
	# 2, 5, 8
	sub $sp, $sp, 4
	sw $ra, 4($sp)
 	lw $t5, 8($s0)
	lw $t6, 20($s0)
	beq $t5, $t6, check_c32		# compare 0, 3, goto check c3
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
 # Diagonals
 check_d11:	
 	# 0, 4, 8
	sub $sp, $sp, 4
	sw $ra, 4($sp)
 	lw $t5, 0($s0)
	lw $t6, 16($s0)
	beq $t5, $t6, check_d12		# compare 0, 4, goto check d1
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
check_d21:
 	# 2, 4, 6
	sub $sp, $sp, 4
	sw $ra, 4($sp)
 	lw $t5, 8($s0)
	lw $t6, 16($s0)
	beq $t5, $t6, check_d22		# compare 2, 4, goto check d2
 	
 	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
 
#####################################
# Rows
check_r12:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 4($s0)
	lw $t6, 8($s0)
	beq $t5, $t6, winner_found	# compare 1, 2, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
check_r22:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 16($s0)
	lw $t6, 20($s0)
	beq $t5, $t6, winner_found	# compare 4, 5, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
check_r32:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 28($s0)
	lw $t6, 32($s0)
	beq $t5, $t6, winner_found	# compare 7, 8, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
# Columns
check_c12:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 12($s0)
	lw $t6, 24($s0)
	beq $t5, $t6, winner_found	# compare 3, 6, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
check_c22:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 16($s0)
	lw $t6, 28($s0)
	beq $t5, $t6, winner_found	# compare 4, 7, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
check_c32:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 20($s0)
	lw $t6, 32($s0)
	beq $t5, $t6, winner_found	# compare 5, 8, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra

# Diagonals
check_d12:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 16($s0)
	lw $t6, 32($s0)
	beq $t5, $t6, winner_found	# compare 4, 8, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
check_d22:
	sub $sp, $sp, 4
	sw $ra, 4($sp)
	
	lw $t5, 16($s0)
	lw $t6, 24($s0)
	beq $t5, $t6, winner_found	# compare 4, 6, goto winner_found
	
	lw $ra, 4($sp)
	add $sp, $sp, 4
	jr $ra
	
###---WINNER_FOUND && PLAYER_WIN && COMPUTER_WIN && TIED---######################################
# winner_found will compare $t5 which holds 'O' or 'X' which was successfully made in a row.	#
# $t5 is compared with $t2, or 'O', to call computer_win, or $t1, or 'X', to call player_win.	#
# The other three functions call their respective text.						#
# It will then call draw_board to display the final board and exit.   				#
#################################################################################################
winner_found:

	# figure out which side has won
	beq $t5, $t2, computer_win
	beq $t5, $t1, player_win
player_win:	
	# print player winning message
	la $a0, winText
	li $v0, 4
	syscall
	
	jal draw_board
	jal exit
	
computer_win:	
	# print player losing message
	la $a0, loseText
	li $v0, 4
	syscall
	
	jal draw_board
	jal exit
	
tied:
	# print tied message
	la $a0, tieText
	li $v0, 4
	syscall
	
	jal draw_board
	jal exit

###---DRAW_BOARD---##############################################################################
# This procedure will print $s0, or board, in a format that is visually pleasing to the player.	#
# for example:	 0 | 1 | 2		 O | 1 | X						#
# 		---+---+---		---+---+---						#
# 		 3 | 4 | 5	  or	 3 | X | O						#
# 		---+---+---		---+---+---						#
# 		 6 | 7 | 8		 X | 7 | 8						#
# If it is called, it will print each element inside the board, whether its 0-8 or 'X' or 'O'	#
#################################################################################################
draw_board:
	
	la $a0, space
	li $v0, 4
	syscall
	
	# number 0 spot
	la $a0, 0($s0)
	li $v0, 4
	syscall
	
	la $a0, bar
	li $v0, 4
	syscall
	
	# number 1 spot
	la $a0, 4($s0)
	li $v0, 4
	syscall
	
	la $a0, bar
	li $v0, 4
	syscall
	
	# number 2 spot
	la $a0, 8($s0)
	li $v0, 4
	syscall
	
	la $a0, divider
	li $v0, 4
	syscall
	
	la $a0, space
	li $v0, 4
	syscall
	
	# number 3 spot
	la $a0, 12($s0)
	li $v0, 4
	syscall
	
	la $a0, bar
	li $v0, 4
	syscall
	
	# number 4 spot
	la $a0, 16($s0)
	li $v0, 4
	syscall
	
	la $a0, bar
	li $v0, 4
	syscall
	
	# number 5 spot
	la $a0, 20($s0)
	li $v0, 4
	syscall
	
	la $a0, divider
	li $v0, 4
	syscall
	
	la $a0, space
	li $v0, 4
	syscall
	
	# number 6 spot
	la $a0, 24($s0)
	li $v0, 4
	syscall
	
	la $a0, bar
	li $v0, 4
	syscall
	
	# number 7 spot
	la $a0, 28($s0)
	li $v0, 4
	syscall
	
	la $a0, bar
	li $v0, 4
	syscall
	
	# number 8 spot
	la $a0, 32($s0)
	li $v0, 4
	syscall

	jr $ra

####---EXIT---###################################
# This procedure is used to end the game.	#
#################################################
exit:
	li $v0, 10
	syscall