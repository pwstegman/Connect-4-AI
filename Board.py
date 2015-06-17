from random import random

class bcolors:
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'

class Board:
	def __init__(self, board=[0 for i in range(42)], nextPiece=1):
		self.width = 7
		self.height = 6
		self.board = board[:]
		self.openSlots = [i for i in range(self.width) if board[i] == 0]
		self.state = "play"
		self.string = self.toString(self.board)
		self.piece = nextPiece
		self.history = []

	def __str__(self):
		return self.string
	
	def toString(self, board):
		return " ".join(map(str, board))

	def display(self):
		print()
		print(*[i+1 for i in range(self.width)])
		for i in range(len(self.board)):
			p = self.board[i]
			if p == 1:
				s = bcolors.BOLD + bcolors.OKGREEN + "x" + bcolors.ENDC*2
			elif p == -1:
				s = bcolors.BOLD + bcolors.OKBLUE + "o" + bcolors.ENDC*2
			else:
				s = "_"
			print(s,"", end="\n" if (i+1)%self.width == 0 else "")
		print()

	def updateState(self, z):
		r = z//self.width
		c = z%self.width
		
		#Check vertical win
		vSize = 0
		cr = r
		while cr < self.height:
			if self.board[cr*self.width+c] == self.board[r*self.width+c]:
				vSize += 1
			else:
				break
			cr += 1

		#Check Horiz win
		hSize = 0
		cc = c
		while cc < self.width:
			if self.board[r*self.width+cc] == self.board[r*self.width+c]:
				hSize += 1
			else:
				break
			cc += 1
		cc = c-1		
		while cc >= 0:
			if self.board[r*self.width+cc] == self.board[r*self.width+c]:
				hSize += 1
			else:
				break
			cc -= 1

		#Check Diag 1 win
		d1Size = 0
		cc = c
		cr = r
		while cc < self.width and cr >= 0:
			if self.board[cr*self.width+cc] == self.board[r*self.width+c]:
				d1Size += 1
			else:
				break
			cc += 1
			cr -= 1
		cc = c-1
		cr = r+1		
		while cc >= 0 and cr < self.height:
			if self.board[cr*self.width+cc] == self.board[r*self.width+c]:
				d1Size += 1
			else:
				break
			cc -= 1
			cr += 1

		#Check Diag 2 win
		d2Size = 0
		cc = c
		cr = r
		while cc >= 0 and cr >= 0:
			if self.board[cr*self.width+cc] == self.board[r*self.width+c]:
				d2Size += 1
			else:
				break
			cc -= 1
			cr -= 1
		cc = c+1
		cr = r+1		
		while cc < self.width and cr < self.height:
			if self.board[cr*self.width+cc] == self.board[r*self.width+c]:
				d2Size += 1
			else:
				break
			cc += 1
			cr += 1

		if vSize >= 4 or hSize >= 4 or d1Size >= 4 or d2Size >= 4:
			self.state = "win"
		elif 0 not in self.board:
			self.state = "tie"
		else:
			self.state = "play"

	def move(self, slot):
		r = self.height - 1
		while self.board[r*self.width+slot] != 0:
			r -= 1
		self.board[r*self.width+slot] = self.piece
		self.history.append([self.string, slot])
		self.string = self.toString(self.board)
		if r == 0:
			self.openSlots.remove(slot)
		self.updateState(r*self.width+slot)
		self.piece *= -1
		return True

	def randomWeightedMove(self, moves):
		slots = [slot for slot in moves]
		weights = [moves[slot] for slot in slots]
		mw = min(weights)
		weights = [w-mw+1 for w in weights]
		total = sum(weights)
		probs = [p/total for p in weights]
		c = random()
		sm = 0
		for r in range(len(probs)):
			sm += probs[r]
			if c < sm:
				slot = slots[r]
				break
		self.move(slot)

	def playRandomGame(self, moves):
		while self.state == "play":
			if len(self.history) < 10:
				if self.string not in moves:
					moves[self.string] = {key: 1 for key in self.openSlots}
				self.randomWeightedMove(moves[self.string])
			else:
				self.randomWeightedMove({key: 1 for key in self.openSlots})

	def requestSlot(self):
		while True:
			try:
				slot = int(input("What slot? "))-1
				if slot not in range(self.width) or self.board[slot] != 0:
					continue
			except ValueError: continue
			break
		return slot
	
	def showResult(self):
		if self.state == "win":
			piece = {-1: bcolors.OKBLUE + "o", 1: bcolors.OKGREEN + "x"}[-self.piece]
			print("Winner:", bcolors.BOLD + piece + bcolors.ENDC*2)
		else:
			print("Tie")



