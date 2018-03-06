from random import randint, seed
from datetime import datetime
from time import sleep
import sys, csv, os, platform
import vlc

# pip install python-vlc

# set random seed
seed(datetime.now())
print("\n\n******   The Amazing Coffee Chooser   ******")
print("================== RULES ==================")
print("1. The coffee must be served within 30 minutes.")
print("2. If the script is used only to collect already made coffee, the coffee maker can be excluded from the selection pool of potential collectors.")
print("3. No whining from Karsten.")
print("4. Everything in The Brocode written by Barney Stinson applies.")
print("5. Whoever participating submits to following these rules to the best of their ability.")
print("Violation of the rules may result in immediate evictions from the bro circle.")
print("============================================\n")

# global variables
macOS = platform.system() == 'Darwin'
work_dir = os.path.dirname(os.path.realpath(__file__))
num_participants = -1
drawed_numbers = []

def makeVLCMediaPlayer(songname):
    player = vlc.MediaPlayer(work_dir + '/resources/' + songname)
    return player

def validateParticipant(num_participants, new_participant, participants):
    # check if newParticipant is unique
    if (new_participant in participants):
        return False

    # check if the number meets constraints
    if (new_participant > 4*num_participants or new_participant < 1):
        return False

    return True

def addParticipants():
    participants = []
    counter = 1

    # user enters how many participants to play
    global num_participants
    while num_participants <= 0:
        num = raw_input("Enter the number of participants: ")
        try:
            num_participants = int(num)
            if (num_participants <= 0): raise Exception
        except:
            print "Invalid input, try again..."

    print("Valid participant numbers are from 1 to %i\n" % (num_participants*4))

    # user enters the individual participants
    while True:
        # check if number of participants is met
        if (counter == num_participants+1):
            break

        num = raw_input("Add participant: ")
        try:
            num = int(num)
            if (validateParticipant(num_participants, num, participants)):
                participants.append(num)
                print("%i added as Participant no. %i." % (num, counter))
                counter += 1
            else:
                print("%i is invalid input, try again..." % (num))

        except:
            print("Invalid input, try again...")

    print("All participants are now added!")
    return participants

# function to say stuff in the terminal
def speak(content):
    # the 'say' command only works on mac os
    if (macOS):
        person = 'Daniel' # Fiona (SC); Nora (NOR); Al (US); Anna (DE); Daniel (DK)
        os.system("say -v " + person + " '" + str(content) + "'")
    else:
        pass

# draw random numbers and see if they match with chosen participants
def drawNumbers(participants):
    randNum = randint(1, 4 * len(participants))

    global drawed_numbers
    drawed_numbers.append(randNum)

    # If a winning number as been picked
    if randNum in participants:
        print("We have a winner!");

        speak("We have a winner!");
        sleep(1)
        speak("And the winner is...")
        sleep(2)
        speak("Number %i!" % randNum)

        print("Number %i is the chosen one! Go get some fucking coffee, participant #%i!!!" % (randNum, (1+participants.index(randNum))))
        return False

    print("Drawed number: %i" % randNum)
    speak(randNum)
    sleep(0.5)
    return True

def updateStatistics(num_participants, drawed_numbers):
    fpath = os.path.dirname(os.path.realpath(__file__)) + '/data/drawed_number_statistics.csv'
    with open(fpath, 'a') as f_a:
        writer = csv.writer(f_a)

        for num in drawed_numbers:
            isWinner = True if (drawed_numbers.index(num) == len(drawed_numbers)-1) else False
            arr = [num_participants, num, isWinner]
            writer.writerow(arr)

def run():
    # create media instances
    player_theme = makeVLCMediaPlayer('millionaire_theme.mp3')
    player_win = makeVLCMediaPlayer('millionaire_win.mp3')

    # start theme music
    player_theme.play()

    # add participants to the game
    participants = addParticipants() # user adds participants

    print("\n*****The Coffee Chooser will now begin*****")
    print("Chosen participants are: %s" % ", ".join([str(x) for x in participants]))

    for timeLeft in reversed(range(0,10)):
        sys.stdout.write('Beginning to draw numbers in %i seconds\r' % timeLeft)
        sys.stdout.flush()
        if (timeLeft == 0):
            print('\nLet the games begin!\n')
            break
        sleep(1)

    # start the game of drawing numbers
    while drawNumbers(participants): continue

    # stop theme music, start winner music
    player_win.play()
    player_theme.stop()

    # update csv file with statistics
    updateStatistics(num_participants, drawed_numbers)

    while (player_win.get_state() == 3):
        # state == 3 = vlc still playing the track
        pass

run()
