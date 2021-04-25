import numpy as np
import itertools
from itertools import permutations
import random


# returns True if newGuess is still a possible solution given guessHistory and ratingHistory, and False otherwise
def eval_guess(newGuess, guessHistory, ratingHistory):

	for i in range(len(guessHistory)):
		
		# overlap is the set of numbers that occur in the guess and the current historical guess
		overlap = set(guessHistory[i]).intersection(newGuess)

		# if newGuess uses more numbers from a historical guess than the rating indicates, return False
		if len(overlap) > (ratingHistory[i][0] + ratingHistory[i][1]):
			return False
		else:
			# score newGuess, if it has more black hits than the historical guess, return False
			temp_score = score_guess(newGuess, guessHistory[i], ratingHistory)
			
			if temp_score[0] != ratingHistory[i][0]:
				return False
	
	return True


def determine_rest(code_list, guessHistory, ratingHistory, p, c, count):

	remaining_codes = code_list
	deletion_indices = list()    

	# if this is the first guess, all remaining codes are legal guesses
	if not guessHistory:
		return remaining_codes

	else:
		# if a code is in guessHistory, remove it from the prospects
		for i in range(len(code_list)):
			if code_list[i] in guessHistory:
				deletion_indices.append(i)

		# if eval_guess determines the current code to not be a possible solution, remove it
		for i in range(len(remaining_codes)):
			if not eval_guess(list(remaining_codes[i]), guessHistory, ratingHistory):
				deletion_indices.append(i)

		for i  in sorted(deletion_indices, reverse = True):
			del remaining_codes[i]

		# print("Remaining codes before guessing: " + str(len(remaining_codes)))
		return list(remaining_codes)


def make_guess(count, p, c, guessHistory, ratingHistory, remaining_codes):

	guess = list()

	remaining_codes = determine_rest(remaining_codes, guessHistory, ratingHistory, p, c, count)

	# print(str(len(remaining_codes)) + " codes remaining.")

	# pick a random guess from all remaining guesses
	rand_pointer = random.randint(0, len(remaining_codes)-1)
	guess = list(remaining_codes[rand_pointer])
	guessHistory.append(guess)
	rem_codes = remaining_codes
	return guess


def score_guess(guess, solution, ratingHistory):

	b = 0
	w = 0
	usedPos = list()
	usedPos.clear()
	blacksFound = list()
	blacksFound.clear()
	whitesFound = list()
	whitesFound.clear()
	score = list()

	for i in range(len(solution)):
		for j in range(len(solution)):
			if solution[i] == guess[j]:
				if i != j:
					# if a number matches the solution, but is not at the same position, increase w and note the positions
					if i not in blacksFound:
						if i not in usedPos:
							w += 1
							whitesFound.append(i)
							usedPos.append(i)
				else:
					# if a number is found at an identical position, increase b
					blacksFound.append(i)
					for k in range(whitesFound.count(i)):
						# if w has already been increased for this position in the solution, decrease w again
						w = w - 1
					b += 1

	score.append(b)
	score.append(w)
	return score


def main():

	print("Welcome to Mastermind.")

	global guesses
	global rating
	# c = colors, p = pegs, gp = possible grades, npc = possible codes with p and c
	global p
	global c
	global gp
	global npc
	# solution = user input code, found = solution found bool, guess history, rating history = nested lists, score = (b, w) hits
	global solution
	global found
	global guessHistory
	global ratingHistory
	global score
	global numberList
	global possible_codes
	global rem_codes

	p = int(input("Play with how many pegs? "))
	c = int(input("Play with how many colors? "))
	gp = (p*(p+3))/2
	npc = pow(c, p)
	found = False
	solution = list()
	solution.clear()
	guessHistory = list()
	ratingHistory = list()
	guesses = 0
	rating = np.array([0, 0])
	score = list()
	numberList = list()
	rem_codes = list()

	for i in range(c):
		for j in range(p):
			numberList.append(i+1)

	# use a set of itertools' permutation to create a powerset including multiples
	print("Initializing code database")
	possible_codes = list(permutations(numberList, p))
	possible_codes = list(set(possible_codes))
	rem_codes = possible_codes

	print("Playing MM(" + str(p) + "," + str(c) + ").")
	print("There are " + str(gp) + " possible grades and " + str(npc) + " possible codes in this game.")
	tempSolution = input("Please enter a " + str(p) + "-digit code and press Enter when ready: ")

	for i in range(p):
		solution.append(int(tempSolution[i]))

	# guess until a solution has been found
	while True:

		currentGuess = make_guess(guesses, p, c, guessHistory, ratingHistory, rem_codes)
		guesses += 1
		score = score_guess(currentGuess, solution, ratingHistory)
		ratingHistory.append(score)

		print("guess # " + str(guesses+1) + ":", end = " ")
		print(currentGuess)
		print("score:", end = " ")
		print(score)

		if score[0] == p:
			print("Solution found:", end = " ")
			print(currentGuess)
			break


if __name__ == "__main__":
    main()
