import pygame
import random
import sys
import os
import time

file_path = '/home/ritz/Desktop/Project/Hangman'
file_name = 'words.txt'

file = os.path.join(file_path, file_name)
#words = open('words.txt', 'r')

w = open(file, 'r')


pygame.init()

display_width = 800
display_height = 600



gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('The Hangman Game')
clock = pygame.time.Clock()

hangImg = pygame.image.load(file_path + '/hang1.png')

words = [i.strip('\n') for i in w.readlines()]
vocab_lentgth = len(words)
#print(len(words))
#time.sleep(5)

g_value = random.randint(1, vocab_lentgth-1)

black = (0, 0, 0)
white = (255, 255, 255)
grey = (150, 150, 150)
bright_grey = (100, 100, 100)
red = (255, 0, 0)
yellow = (240, 240, 0)
green = (0, 255, 0)
font = 0

mouseOver = False

length_y = 10
lenght_x = 5
side = 25

won = False

w_len = len(words[g_value])
dashes = w_len//2

r = sorted(random.sample(range(w_len), dashes))

word_track = [0]*w_len

enabled = {'A':0, 'B':0, 'C':0, 'D':0, 'E':0, 'F':0, 'G':0, 'H':0, 'I':0, 'J':0, 'K':0,
 'L':0, 'M':0, 'N':0, 'O':0, 'P':0, 'Q':0, 'R':0, 'S':0, 'T':0,'U':0, 'V':0, 'W':0, 'X':0, 'Y':0, 'Z':0}



pos_x_first = [240, 275, 310, 345, 380, 415, 450, 485, 520, 555, 590, 275,310,345,380,415,450,485,520,555,325,360,395,430,465,500]
letters1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T','U', 'V', 'W', 'X', 'Y', 'Z']
alpha_y1 = 280
alpha_y2 = 320
alpha_y3 = 360
count = 0
total_try = 0
Lost = False

def clearValues():
	global won, w_len, word_track, dashes, g_value, r, total_try, Lost
	g_value = random.randint(1, vocab_lentgth-1)
	w_len = len(words[g_value])
	dashes = w_len//2
	r = sorted(random.sample(range(w_len), dashes))
	word_track = [0]*w_len
	won = False
	Lost = False
	clearEnabled()


def clearEnabled():
	for key in enabled.keys():
		enabled[key] = 0


def getSize(size):
	global font
	if size == "extrasmall":
		font = pygame.font.Font('freesansbold.ttf', 18)
	elif size == "small":
		font = pygame.font.Font('freesansbold.ttf', 30)
	elif size == "medium":
		font = pygame.font.Font('freesansbold.ttf', 60)
	elif size == "large":
		font = pygame.font.Font('freesansbold.ttf', 80)


def write_on_screen(msg, x=display_width/2, y=display_height/2, size="small" ,side=0, color=black, x_displace=0, y_displace=0):

	textStyle, textRect = text_objects(msg, color, size)
	textRect.center = (x+side/2+x_displace, y+side/2+y_displace)
	gameDisplay.blit(textStyle, textRect)


def text_objects(text, color, size):

	getSize(size)
	textStyle = font.render(text, True, color)
	return textStyle, textStyle.get_rect()


def checkAlphabet(msg):
	global won, Lost
	w_list = list(words[g_value].upper())
	#print(w_list)
	#time.sleep(1 )
	all_match = [x for x in range(len(w_list)) if w_list[x] == msg]

	m = len(all_match)
	if m == 0:
		if msg != "NEXT" and msg != "nothing":
			enabled[msg] = True
	#time.sleep(1)
	for i in range(m):
		enabled[msg] = False
		word_track[all_match[i]] = msg
		try:
			r.remove(all_match[i])
		except ValueError:
			pass

	if 0 not in word_track:
		won = True
		print("".join(word_track))
		print(won)


def onHover(x, y, mouse,lead_y=0, color=grey, rect_l=25, rect_b=25, msg="nothing"):

	print(enabled)
	global total_try, Lost
	
	click = pygame.mouse.get_pressed()

	if x+rect_l > mouse[0] > x and y+rect_b+lead_y > mouse[1] > y+lead_y:
		if msg != 'NEXT' and msg != 'nothing' and enabled[msg] == True:
			gameDisplay.fill(red, rect=[x, y+lead_y, rect_l, rect_b])
		else:
			gameDisplay.fill(bright_grey, rect=[x, y+lead_y, rect_l, rect_b])

		total_try = len([i for i in enabled.values() if i == True])
		print(total_try)
		if total_try <= 6:
			if click[0] == 1:
				if msg == "NEXT" and won == True:
					#print("value", value)
					clearValues()
				elif msg == "nothing":
					pass
				else:
					if not won:
						#print(won)
						checkAlphabet(msg)
					else:
						#print("already won")
						clearEnabled()

		else:
			Lost = True
			print("I Lost")
			#time.sleep(10)
			if click[0] == 1:
				if msg == "NEXT" and won == False:
					clearValues()
				elif msg == "nothing":
					pass
				else:
					print(total_try, Lost)
					time.sleep(2)
					#clearEnabled()
			#clearValues()
			#clearEnabled()
	else:
		if msg != 'NEXT' and msg != 'nothing' and enabled[msg] == True:
			gameDisplay.fill(red, rect=[x, y+lead_y, rect_l, rect_b])
		else:
			gameDisplay.fill(grey, rect=[x, y+lead_y, rect_l, rect_b])


def wordDisp():
	l = 0
	global w_list, word_track
	word = words[g_value].upper()
	w_list = list(word)
	#print(w_list, word_track)
	for i in range(len(w_list)):
		l += 24
		if i in r:
			write_on_screen("_", 315+l, 150, "small")
			
		else:
			word_track[i] = w_list[i]
			write_on_screen(w_list[i], 315+l, 150, "small")

	#print (word_track)



def mainGame():
	global total_try
	exitGame = False
	while not exitGame:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exitGame = True

			#print(event)
		gameDisplay.fill(white)

		gameDisplay.blit(hangImg, (display_width*0.45, display_height * 0.7))
		
		wordDisp()
		mouse = pygame.mouse.get_pos()
		count = 0
		for i, j in zip(pos_x_first, letters1):
			if count < 11:
				onHover(i, alpha_y1, mouse, msg=j)
				write_on_screen(j, i, alpha_y1, "extrasmall", side=25, color=yellow)
			if count >= 11 and count < 20:
				#print(i,count)
				#time.sleep(1)
				onHover(i, alpha_y1, mouse, 40, msg=j)
				write_on_screen(j, i, alpha_y2, "extrasmall", side=25, color=yellow)
			if count >= 20 and count < 26:
				onHover(i, alpha_y1,mouse, 80, msg=j)
				write_on_screen(j, i, alpha_y3, "extrasmall", side=25, color=yellow)
			count += 1

		write_on_screen("Guess The Word", size="small", color=red, y_displace=-270)

		onHover(700, 230, mouse, color=grey, rect_l=50, rect_b=30, msg="NEXT")
		write_on_screen("NEXT", 700, 230, "extrasmall", color=yellow, x_displace=25, y_displace=15)

		if 0 not in word_track:
			write_on_screen("YOU WON!", 390, 230, size="small", color=red)
		elif Lost == True:
			write_on_screen("YOU LOOSE!", 390, 230, size="small", color=red)

		pygame.display.update()

		clock.tick(100)

mainGame()
pygame.quit()
quit()





