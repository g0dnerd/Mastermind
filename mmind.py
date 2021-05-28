import itertools
from itertools import permutations
import random
from timer import Timer

# returns True if newGuess is still a possible solution given guessHistory and ratingHistory, and False otherwise
def eval_guess(newGuess, guessHistory, ratingHistory):

	for i in range(len(guessHistory)):
		
		tempScore = score_guess(newGuess, guessHistory[i], ratingHistory)
		overlap = tempScore[0] + tempScore[1]


		# if newGuess uses more numbers from a historical guess than the rating indicates, return False
		if overlap != (ratingHistory[i][0] + ratingHistory[i][1]):
			return False
		else:
			# score newGuess, if it has more black hits than the historical guess, return False
			tempScore = score_guess(newGuess, guessHistory[i], ratingHistory)
			
			if tempScore[0] != ratingHistory[i][0]:
				return False
	
	return True


def determine_rest(codeList, guessHistory, ratingHistory):

	codesLeft = list(codeList)
	deletionIndices = list()    

	# if this is the first guess, all remaining codes are legal guesses
	if not guessHistory:
		return codesLeft

	else:
		# if a code is in guessHistory, remove it from the prospects
		for i in range(len(codeList)):
			if codeList[i] in guessHistory:
				deletionIndices.append(i)

		# if eval_guess determines the current code to not be a possible solution, remove it
		for i in range(len(codesLeft)):
			if not eval_guess(list(codesLeft[i]), guessHistory, ratingHistory):
				deletionIndices.append(i)

		deletionIndices = list(dict.fromkeys(deletionIndices))

		# print("Marked for deletion:")
		# print(deletionIndices)

		for i in sorted(deletionIndices, reverse = True):
			del codesLeft[i]

		# print("Remaining codes before guessing: " + str(len(codesLeft)))
		return list(codesLeft)

def count_eliminations(remainingCodes, guess, rating, guessHistory, ratingHistory):

	tempGuessHistory = list(guessHistory)
	tempGuessHistory.append(list(guess))
	tempRatingHistory = list(ratingHistory)
	tempRatingHistory.append(list(rating))

	elimAmount = len(remainingCodes) - len(determine_rest(remainingCodes, tempGuessHistory, tempRatingHistory))

	return elimAmount

def minmax_guess(guessHistory, ratingHistory, remainingCodes):

	# print("minmax called with remaining len: " + str(len(remainingCodes)))

	tempRating = list()
	eliminationCount = list()
	eliminationGuesses = list()
	eliminationRatings = list()
	eliminationMinMax = {"guess":[], "elim":[], "rating": []}

	for i in range(len(unusedCodes)):
		for b in range(5):
			for w in range(5):
				tempRating.clear()
				if b + w < 5 and not (b == 3 and w == 1):
					tempRating.append(b)
					tempRating.append(w)
					# print(tempRating)
					# print(len(remainingCodes))
					# print(i)
					tempGuess = unusedCodes[i]
					tempElim = count_eliminations(remainingCodes, tempGuess, tempRating, guessHistory, ratingHistory)
					eliminationMinMax["guess"].append(list(tempGuess))
					eliminationMinMax["elim"].append(tempElim)
					eliminationMinMax["rating"].append(list(tempRating))


	# look for the code that among all possible ratings has the lowest maximum of possible codes eliminated

	prevGuess = list()
	minElimList = list()
	tempMinElim = 0
	bestGuesses = list()

	# print(str(len(eliminationMinMax["guess"])))

	for i in range(len(eliminationMinMax["guess"])):

		currentGuess = eliminationMinMax["guess"][i]
		currentElim = eliminationMinMax["elim"][i]

		if i == 0:
			tempMinElim = currentElim
			prevGuess = currentGuess
		else:
			if currentGuess == prevGuess:
				if currentElim < tempMinElim:
					tempMinElim = currentElim
					prevGuess = currentGuess
			else:
				minElimList.append(tempMinElim)
				bestGuesses.append(currentGuess)
				tempMinElim = currentElim
				prevGuess = currentGuess
				
	minmaxIndex = minElimList.index(max(minElimList))

	return bestGuesses[minmaxIndex]	


def make_guess(guessHistory, ratingHistory, remainingCodes):

	# print("make_guess called with " + str(len(unusedCodes)) + " unused codes remaining.")

	guess = list()

	if guesses != 0:	
		
		remainingCodes = determine_rest(remainingCodes, guessHistory, ratingHistory)
		print(str(len(remainingCodes)) + " codes remain possible.")		
		print("Scanning " + str(len(remainingCodes)*14) + " possibilities...")
		
		# if len(remainingCodes) < 15:
		#	print(remainingCodes)
		
		if len(remainingCodes) < 3:
			guess = list(remainingCodes[0])
			guessHistory.append(guess)
			unusedCodes.remove(list(guess))
			return guess

		guess = minmax_guess(guessHistory, ratingHistory, remainingCodes)
		guessHistory.append(guess)
		unusedCodes.remove(list(guess))
		return guess
		# TODO

	else:
		# the best first guess differs on approach.
		guess = (1, 1, 2, 2)
		guessHistory.append(guess)
		unusedCodes.remove(list(guess))
		return guess



def score_guess(guess, solution, ratingHistory):

	b = 0
	w = 0
	score = list()
	score.clear()

	for i in range(len(solution)):
		for j in range(len(solution)):
			if solution[i] == guess[j]:
				if i == j:
					# if a number is found at an identical position, increase b
					b += 1

	w = 0
	for i in range(c):
		w = w + min(solution.count(i+1), guess.count(i+1))

	w = w - b

	score.append(b)
	score.append(w)

	# print("Grading guess", end = " ")
	# print(guess)
	# print(solution)
	# print(score)
	return score


def main():

	t = Timer()
	t.start()

	print("Welcome to Mastermind.")

	global guesses
	global rating
	# c = colors, p = pegs, gp = possible grades, npc = possible codes with p and c
	global p
	global c
	global gp
	global npc
	# solution = user input code, found = solution found bool
	# guess history, rating history = nested lists, score = (b, w) hits
	global solution
	global found
	global guessHistory
	global ratingHistory
	global score
	global numberList
	global possibleCodes
	global remCodes
	global unusedCodes

	p = 4
	c = 6
	gp = (p*(p+3))/2
	npc = pow(c, p)
	found = False
	solution = list()
	solution.clear()
	guessHistory = list()
	ratingHistory = list()
	guesses = 0
	score = list()
	numberList = list()
	remCodes = list()
	unusedCodes = list()

	for i in range(c):
		for j in range(p):
			numberList.append(i+1)

	# use a set of itertools' permutation to create a powerset including multiples
	print("Initializing code database...")
	possibleCodes = list(permutations(numberList, p))
	possibleCodes = list(dict.fromkeys(possibleCodes))

	remCodes = possibleCodes

	for i in range(len(possibleCodes)):
		unusedCodes.append(list(possibleCodes[i]))

	print("Playing MM(" + str(p) + "," + str(c) + ").")
	print("There are " + str(gp) + " possible grades and " + str(npc) + " possible codes in this game.")
	tempSolution = input("Please enter a " + str(p) + "-digit code and press Enter when ready: ")

	for i in range(p):
		solution.append(int(tempSolution[i]))

	while True:

		printGuess = make_guess(guessHistory, ratingHistory, remCodes)
		guesses += 1
		score = score_guess(printGuess, solution, ratingHistory)
		ratingHistory.append(score)

		print("guess # " + str(guesses) + ":", end = " ")
		print(printGuess)
		print("score:", end = " ")
		print(score)

		if score[0] == p:
			print("Solution found:", end = " ")
			print(printGuess)
			t.stop()
			break


if __name__ == "__main__":
    main()