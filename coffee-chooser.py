# -*- coding: utf-8 -*-
from random import randint, seed
from datetime import datetime
from time import sleep
from vlc import MediaPlayer
import sys, os, platform

# set seed to ensure complete randomness in the drawing process
seed(datetime.now())

# set global variables
macOS = platform.system() == 'Darwin'
work_dir = os.path.dirname(os.path.realpath(__file__))
resources_folder = work_dir + '/resources/'
num_participants = -1

# print the rules of the Coffee Chooser
print("\n\n******   The Amazing Coffee Chooser   ******")
print("================== RULES ==================")
print("1. The coffee must be served within 30 minutes.")
print("2. If the script is used only to collect already made coffee, "
      "the coffee maker can be excluded from the selection pool of potential collectors.")
print("3. No whining from Karsten.")
print("4. If it's made insufficient quantities of coffee, then more coffee must be made.")
print("5. Whoever participating submits to following these rules to the best of their ability.")
print("Violation of the rules may result in immediate evictions from the bro circle.")
print("============================================\n")


def make_vlc_player(songname):
    ''' Returns a VLC Media Player object '''
    player = MediaPlayer(resources_folder + songname)
    return player


def validate_participant(n_participants, new_participant, participants):
    ''' Check that a new participant is valid '''
    if new_participant in participants:
        return False

    # check if the number (participant) meets constraints
    if new_participant > 4 * n_participants or new_participant < 1:
        return False

    return True


def add_participants():
    ''' Method to iteratively add participants '''
    participants = []
    counter = 1

    # user enters how many participants to play
    global num_participants
    while num_participants <= 0:
        num = input("Enter the number of participants: ")
        try:
            num_participants = int(num)
            if num_participants <= 0:
                raise Exception()
        except:
            print("Invalid input, try again...")

    print("Valid participant numbers are from 1 to %i\n" %
          (num_participants * 4))

    # user enters the individual participants
    while True:
        # check if number of participants is met
        if counter == num_participants + 1:
            break

        num = input("Add participant: ")
        try:
            num = int(num)
            if validate_participant(num_participants, num, participants):
                participants.append(num)
                print("%i added as Participant no. %i." % (num, counter))
                counter += 1
            else:
                raise Exception()

        except:
            print("Invalid input, try again...")

    print("All participants are now added!")
    return participants


def speak(content):
    ''' Function to say stuff in the terminal '''

    # the 'say' command only works on mac os
    if macOS:
        # Fiona (SC); Nora (NOR); Al (US); Anna (DE); Danielter (DK)
        person = 'Daniel'
        os.system("say -v " + person + " '" + str(content) + "'")
    else:
        pass


def draw_numbers(participants):
    ''' Iteratively draws numbers until a winner has been picked '''
    while True:
        rand_num = randint(1, 4 * len(participants))
        if rand_num in participants:
            print("We have a winner!")

            speak("We have a winner!")
            sleep(1)
            speak("And the winner is...")
            sleep(2)
            speak("Number %i!" % rand_num)

            print("Number %i is the lucky winner! Go get some fu***** coffee, participant #%i!!! ☕️☕️️️" % (
                rand_num, (1 + participants.index(rand_num))))
            break

        else:
            print("Drawn number: %i" % rand_num)
            speak(rand_num)
            sleep(5)


def run():
    ''' The main function that runs the entire program '''

    # create media instances
    player_theme = make_vlc_player('millionaire_theme.mp3')
    player_win = make_vlc_player('millionaire_win.mp3')

    # start theme music
    player_theme.play()

    # add participants to the game
    participants = add_participants()  # user adds participants

    print("\n*****The Coffee Chooser will now begin*****")
    print("Chosen participants are: %s" %
          ", ".join([str(x) for x in participants]))

    for time_left in reversed(range(0, 10)):
        sys.stdout.write(
            'Beginning to draw numbers in %i seconds\r' % time_left)
        sys.stdout.flush()
        if time_left == 0:
            print('\nLet the games begin!\n')
            break
        sleep(1)

    # start the game of drawing numbers
    draw_numbers(participants)

    player_win.play()  # start winner music
    player_theme.stop()  # stop theme music
    sleep(25)  # let the song play for 25 seconds
    player_win.stop()  # then stop


if __name__ == '__main__':
    run()
