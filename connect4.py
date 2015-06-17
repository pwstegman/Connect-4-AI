#!/usr/bin/env python3

"""
Connect 4 AI

Plays 2000 games each round to calculate the probability of each possible move being a good move
"""

__author__ = "Pierce Stegman"
__copyright__ = "Copyright 2015, Pierce Stegman"
__email__ = "pwstegman@gmail.com"

import signal
import sys
from Board import Board, bcolors

def humanMove(B):
	B.move(B.requestSlot())
	B.display()

def computerMove(B, diff, piece):
	p = runSims(B, diff, piece)
	B.move(max(p, key=p.get))
	B.display()

def play(B, diff, p1, p2):
	if p1 == "human":
		humanMove(B)
	else:
		computerMove(B, diff, 1)
	if B.state == "play":
		if p2 == "human":
			humanMove(B)
		else:
			computerMove(B, diff, -1)

def onExit(signal, frame):
		print()
		sys.exit(0)

def settings():
	p1 = ""
	while p1 not in ["computer","human"]:
		p1 = input("Player 1: [computer/"+bcolors.UNDERLINE+"human"+bcolors.ENDC+"]: ") or "human"
		if p1 == "h": p1 = "human"
		if p1 == "c": p1 = "computer"
	print(p1)
	p2 = ""
	while p2 not in ["computer","human"]:
		p2 = input("Player 2: ["+bcolors.UNDERLINE+"computer"+bcolors.ENDC+"/human]: ") or "computer"
		if p2 == "h": p2 = "human"
		if p2 == "c": p2 = "computer"
	print(p2)
	diff = ""
	if p1 == p2 == "human":
		diff = "0"
	else:
		while not diff.isdigit() or int(diff) < 1:
			diff = input("Simulations to run each round [default 2000]: ") or "2000"
		diff = int(diff)
		print(diff)
	return p1, p2, diff

def main():

	signal.signal(signal.SIGINT, onExit)
	
	print("Connect 4 AI by Pierce Stegman")
	print()
	
	p1, p2, diff = settings()
	
	command = input("What would you like to do? ["+bcolors.UNDERLINE+"play"+bcolors.ENDC+"/settings/exit] ") or "play"
	if command == "settings":
		p1, p2, diff = settings()
		
	while command != "exit":
		B = Board()
		B.display()
		while B.state == "play":
			play(B, diff, p1, p2)
		B.showResult()
		
		command = input("What would you like to do? ["+bcolors.UNDERLINE+"play"+bcolors.ENDC+"/settings/exit] ") or "play"
		if command == "settings":
			p1, p2, diff = settings()

def runSims(B, diff, piece):
	probs = {}
	for i in range(diff):
		temp = Board(B.board, piece)
		temp.playRandomGame(probs)
		if temp.state == "win" and temp.piece == piece:
			histLen = len(temp.history)
			limit = 10
			if histLen < 10:
				limit = histLen
			for h in range(0,limit,2):
				hist = temp.history[h]
				probs[hist[0]][hist[1]] -= 1/histLen**1.5
	return probs[B.string]

if __name__ == '__main__':
	main()
