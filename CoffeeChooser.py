from random import randint, seed
from datetime import datetime
import time, sys, subprocess, csv, os

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
num_participants = -1
drawed_numbers = []

# sets iTunes to play intense music from 'Do you want to be a millionaire'
def playIntenseMusic():
    # subprocess.call(['open', 'Resources/millionaire_theme.mp3']) # this will actually open iTunes

    # play and pause track immediately
    subprocess.Popen(['osascript', '-e', 'tell application \"iTunes\" to play track \"Millionaire_theme\" of playlist \"Millionaire\"'])
    subprocess.call(['osascript', '-e', 'tell application \"iTunes\" to pause'])

    # reset track
    subprocess.Popen(['osascript', '-e', 'tell application \"iTunes\" to set player position to 0'])
    subprocess.Popen(['osascript', '-e', 'tell application \"iTunes\" to play track \"Millionaire_theme\" of playlist \"Millionaire\"'])

def validateParticipant(num_participants, new_participant, participants):
    # check if newParticipant is unique
    if (new_participant in participants):
        return False

    # check if the number meets constraints
    if (new_participant > 4*num_participants or new_participant < 0):
        return False

    return True

def addParticipants():
    participants = []
    counter = 1

    # user enters how many participants to play
    global num_participants
    while num_participants <= 0:
        num_participants = int(raw_input("Enter the number of participants (Press enter to continue): "))

    print("Valid participant numbers are between 0 and %i\n" % (num_participants*4))

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
            if num == '': break
            else: print("Invalid input, try again...")

    print("All participants are now added!")
    return participants

# function to "say stuff" in the terminal
def speak(content):
    person = 'Agnes' # Fiona (SC); Nora (NOR); Agnes (US); Anna (DE)
    os.system("say -v " + person + " '" + str(content) + "'")

# draw random numbers and see if they match with chosen participants
def drawNumbers(participants):
    randNum = randint(0, 4 * len(participants))

    global drawed_numbers
    drawed_numbers.append(randNum)

    # If a winning number as been picked
    if randNum in participants:
        print("We have a winner!"); speak("We have a winner!");
        speak("And the winner is...")
        time.sleep(2)
        speak("Number %i!" % randNum)

        print("Number %i is the chosen one! Go get some fucking coffee, participant #%i!!!" % (randNum, (1+participants.index(randNum))))
        subprocess.Popen(['osascript', '-e', 'tell application \"iTunes\" to play track \"Millionaire_win\" of playlist \"Millionaire\"'])

        return False

    print("Drawed number: %i" % randNum)
    speak(randNum)
    time.sleep(5)
    return True

def updateStatistics(num_participants, drawed_numbers):
    with open('data/drawed_number_statistics.csv', 'a') as f_a:
        writer = csv.writer(f_a)

        for num in drawed_numbers:
            isWinner = True if (drawed_numbers.index(num) == len(drawed_numbers)-1) else False
            arr = [num_participants, num, isWinner]
            writer.writerow(arr)

def run():
    playIntenseMusic()
    participants = addParticipants() # user adds participants

    print("\n*****The Coffee Chooser will now begin*****")
    print("Chosen participants are: %s" % ", ".join([str(x) for x in participants]))

    for timeLeft in reversed(range(0,10)):
        sys.stdout.write('Beginning to draw numbers in %i seconds\r' % timeLeft)
        sys.stdout.flush()
        if (timeLeft == 0):
            print('\nLet the games begin!\n')
            break
        time.sleep(1)

    while drawNumbers(participants): continue

    # update csv file with statistics
    updateStatistics(num_participants, drawed_numbers)

    time.sleep(25) # let the music play for 25 seconds
    subprocess.call(['osascript', '-e', 'tell application \"iTunes\" to pause']) # stop the track

run()
