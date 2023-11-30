# *****************************************************************************
# Author:           Patrick Foster
# Lab:              Lab 5
# Date:             3/3/22
# Description:          This program is an update to Lab 4. The program's
#                   basic functionality is the same as Lab 4 where the player
#                   creates a character and fights an enemy. Higher strength
#                   leads to higher attack. Higher agility gives the player
#                   higher defense. If a player defends, they have a chance
#                   to get a critical attack the next round. If no damage is
#                   dealt, there is a message saying the attack tried to get
#                   evaded, but there is still a chance to do some damage.
#                   Critical attack chance is based on a character's agility.
#
# Input:            Ask for a character name.
#                   Ask to put points into strength and agility.
#                   Ask if player is happy with choices.
#                   Ask if player wants to run or fight.
#                   Ask if player wants to attack or defend.
#
# Output:           The output will display various information about the game.
#
# Sources:          Lab 5 specifications.
#                   Updating Lab 4's code and functionality.
# *****************************************************************************

import random

# Setting the hitpoints could make a fight longer or shorter.
# Used for both player and enemy.
BASE_HITPOINTS = 100

# Used to determine the player's starting stats.
# Not using it for the enemy's stats since they are created based on using 10 points.
BASE_ABILITY_POINTS = 10

# Character lists: [name, health, strength, agility, attack, defense, critChance, hasCrit]
# Used to help with listing what the array indices are
NAME = 0
HEALTH = 1
STRENGTH = 2
AGILITY = 3
ATTACK = 4
DEFENSE = 5
CRIT_CHANCE = 6
HAS_CRIT = 7

# Enemy Blueprints for spawning enemies and allows for an easy way to add
#   more enemies without have to go into the create enemy function.
# Also need to be sure to add the new enemy into the spawn rate global or
#   else it won't spawn.
# Enemy blueprints have [name, minStr, maxStr, minCritChance, maxCritChance]
ENEMY_BLUEPRINT = {
    0: ["Troll", 5, 9, 2, 3],
    1: ["Goblin", 1, 5, 3, 5],
    2: ["Kobold", 3, 7, 4, 6]
}

# Enemy Spawn Rate is for customizing how rare an enemy should spawn.
#   As an example, with spawn rate of [0, 1, 1], this will allow the goblins
#   to have twice the chance to spawn since there are two 1's from the
#   blueprint.
ENEMY_SPAWN_RATE = [2, 1, 2, 0, 1, 2]


def main():
    # Display Instructions
    printDoubleBar()
    print("      Your name can only be letters and/or numbers.")
    print("      It can include spaces and/or hyphens.")
    printSingleBar()
    print("      To answer a question or do an action,")
    print("      you can either enter the full word or")
    print("      the first letter of the word.")
    printSingleBar()
    print("      To try to get a critical attack, you")
    print("      need to defend first and then attack.")
    printDoubleBar()

    lstPlayer = createPlayer()
    lstEnemy = createEnemy()

    printDoubleBar()
    print("You have encountered a " + lstEnemy[NAME] + "!")
    printEmptySpace()

    print("It looks " + strengthToString(lstEnemy[STRENGTH]) + ".")
    print("It looks " + agilityToString(lstEnemy[AGILITY]) + ".")
    printEmptySpace()

    answer = askTwoChoices("run", "fight", "Will you (r)un or (f)ight? ")
    printDoubleBar()

    if checkAnswer(answer, "run"):
        print("Like a coward, you ran away. At least you")
        print("survived to run another day!")
    elif checkAnswer(answer, "fight"):
        print("You have entered combat!")
        while lstPlayer[HEALTH] > 0 and lstEnemy[HEALTH] > 0:
            printSingleBar()
            print("Your health is:", lstPlayer[HEALTH])
            print("Enemy's health is:", lstEnemy[HEALTH])
            printEmptySpace()

            answer = askTwoChoices("attack", "defend",
                                   "Will you (a)ttack or (d)efend? ")
            printDoubleBar()

            if checkAnswer(answer, "attack"):
                lstEnemy[HEALTH] = doCombat(lstEnemy, lstPlayer)
                lstPlayer[HAS_CRIT] = False
            elif checkAnswer(answer, "defend"):
                if lstPlayer[HAS_CRIT]:
                    print("You have already defended last round.")
                    answer = askTwoChoices("yes", "no", "Are you sure (y)es/"
                                                        "(n)o? ")
                    if checkAnswer(answer, "yes"):
                        printSingleBar()
                        print("You decided to defend anyway.")
                    else:
                        printSingleBar()
                        print("You decide to attack instead.")
                        lstEnemy[HEALTH] = doCombat(lstEnemy, lstPlayer)
                        lstPlayer[HAS_CRIT] = False
                else:
                    print("You decided to defend this round.")
                    # Making sure the player keeps their crit
                    lstPlayer[HAS_CRIT] = True

            printEmptySpace()

            if lstEnemy[HEALTH] > 0:
                if not lstEnemy[HAS_CRIT] and getRandomInt(0, 3) == 1:
                    print("The", lstEnemy[NAME],
                          "decided to defend this turn.")
                    lstEnemy[HAS_CRIT] = True
                else:
                    lstPlayer[HEALTH] = doCombat(lstPlayer, lstEnemy)
                    lstEnemy[HAS_CRIT] = False

        printDoubleBar()

        if lstPlayer[HEALTH] > 0:
            print("You have WON the fight!")
        else:
            print("You have LOST the fight!")

    printDoubleBar()


def doCombat(lstDefender, lstAttacker):
    # Dividing defense and attack by 2 to get the base agility and
    # strength for now just to get a simple range for random
    newDefense = getRandomInt(lstDefender[DEFENSE] / 2, lstDefender[DEFENSE])
    newAttack = getRandomInt(lstAttacker[ATTACK] / 2, lstAttacker[ATTACK])

    # If the defender has a critical then they defended
    # last turn so add a bit to their defense.
    if lstDefender[HAS_CRIT]:
        print(lstDefender[NAME], "tried to block!")
        newDefense += 2

    if lstAttacker[HAS_CRIT]:
        if getRandomInt(0, lstAttacker[CRIT_CHANCE]) == 1:
            newAttack *= 2
            print(lstAttacker[NAME], "got a CRITICAL attack!")

    newAttack -= newDefense

    # If the attack actually is 0 or less, I'm doing a quick workaround
    #   to allow combat to keep flowing instead of being stuck at everyone
    #   doing 0 damage all the time. Just want to do it this way instead of
    #   thinking of a good algorithm because I want to keep the combat
    #   simple for now.
    if newAttack <= 0:
        # Still has a chance to do 0 damage, but can go up to the attacker's
        # strength also.
        newAttack = getRandomInt(0, lstAttacker[STRENGTH])
        print(lstDefender[NAME], "tried to evade!")

    print(lstDefender[NAME], "was attacked by", lstAttacker[NAME],
          "and took " + str(newAttack) + " damage!")

    return lstDefender[HEALTH] - newAttack


def createPlayer():
    accept = "no"
    name = ""
    strength = 0
    agility = 0
    hitPoints = 0
    attack = 0
    defense = 0
    critChance = 0

    while checkAnswer(accept, "no"):
        while True:
            name = str(input("What is your name? "))

            if checkName(name, 15):
                break

        printSingleBar()

        print("You have", BASE_ABILITY_POINTS, "ability points to spend.")
        print("Strength is good for attack.")
        print("Agility is good for defense and crit chance.")

        while True:
            printEmptySpace()

            # NOTE: Going to limit the player to have to choose a number
            #       between 1 and (BASE_ABILITY_POINTS -1) so they can't
            #       choose 0 for strength since this would make it so
            #       they can't do damage.
            strength = askForNumber(1, BASE_ABILITY_POINTS - 1,
                                    "Enter your strength (1 to " +
                                    str(BASE_ABILITY_POINTS - 1) +
                                    "): ", False)

            printEmptySpace()

            agility = askForNumber(1, BASE_ABILITY_POINTS - strength,
                                   "Enter your agility (1 to " +
                                   str(BASE_ABILITY_POINTS - strength) +
                                   "): ", False)

            if strength + agility < BASE_ABILITY_POINTS:
                printEmptySpace()

                print("You did not use all of your points.")
                accept = askTwoChoices("yes", "no", "Are you sure you want "
                                                    "to continue (y)es/(n)o? ")

                if checkAnswer(accept, "yes"):
                    break
            else:
                break

        printSingleBar()

        hitPoints = BASE_HITPOINTS
        attack = strength * 2
        defense = agility * 2
        critChance = getRandomInt(1, 10 - agility)

        print("Your character currently is:")
        print("    Name:", name)
        print("    Hit Points:", hitPoints)
        print("    Strength:", strength)
        print("    Agility:", agility)
        print("    Attack:", attack)
        print("    Defense:", defense)
        print("    Crit Chance: " + str(getCritPercent(critChance)) + "%")
        printEmptySpace()

        accept = askTwoChoices("yes", "no", "Do you accept your character "
                                            "(y)es/(n)o? ")

        if checkAnswer(accept, "no"):
            strength = 0
            agility = 0
            printSingleBar()
            print("Lets try again.")

    printDoubleBar()
    print("Character creation was successful.")

    return [name, hitPoints, strength, agility, attack, defense,
            critChance, False]


def createEnemy():
    abilityPoints = 10
    hitPoints = BASE_HITPOINTS

    # Choose which enemy will be spawned from the spawn rate list
    enemySpawned = ENEMY_SPAWN_RATE[getRandomInt(0, len(ENEMY_SPAWN_RATE) - 1)]

    # Enemy Blueprint:
    #   0      1       2           3             4
    # [name, minStr, maxStr, minCritChance, maxCritChance]
    # Fill out the enemy's information based on their blueprint
    name = ENEMY_BLUEPRINT[enemySpawned][0]
    # Strength will be set a random number between minStrength and maxStrength
    strength = getRandomInt(ENEMY_BLUEPRINT[enemySpawned][1],
                            ENEMY_BLUEPRINT[enemySpawned][2])

    agility = abilityPoints - strength
    attack = strength * 2
    defense = agility * 2
    critChance = getRandomInt(ENEMY_BLUEPRINT[enemySpawned][3],
                              ENEMY_BLUEPRINT[enemySpawned][4])

    return [name, hitPoints, strength, agility, attack, defense,
            critChance, False]


def strengthToString(strength):
    if strength >= 7:
        return "strong"
    elif 4 <= strength <= 6:
        return "average in strength"
    else:
        return "weak"


def agilityToString(agility):
    if agility >= 7:
        return "quick"
    elif 4 <= agility <= 6:
        return "average in agility"
    else:
        return "slow"


# This function is used to convert critChance to a percentage as an integer
def getCritPercent(critChance):
    return int(round((1 / (critChance + 1)) * 100))


# This function is used for yes or no questions
def askTwoChoices(choiceOne, choiceTwo, question):
    answer = str(input(question)).lower()
    while not checkAnswer(answer, choiceOne) and \
            not checkAnswer(answer, choiceTwo):
        printSingleBar()
        print("Please choose either '" + choiceOne + "' or '"
              + choiceTwo + "'.")
        answer = str(input(question)).lower()

    return answer


# This function is used to check against an answer.
def checkAnswer(playerAnswer, correctAnswer, canUseFirst=True):
    if playerAnswer == correctAnswer:
        return True
    # If the answer can use only the first letter, make sure it
    #   only has a length of 1 then check the answer.
    elif canUseFirst and len(playerAnswer) == 1:
        if playerAnswer[0] == correctAnswer[0]:
            return True

    return False


def askForNumber(lowerLimit, upperLimit, question, showLimit=True):
    while True:
        try:
            if showLimit:
                print("Choose a number from", lowerLimit,
                      "to " + str(upperLimit) + ".")

            number = int(input(question))

            if number < lowerLimit or number > upperLimit:
                printSingleBar()
                print("You made an invalid choice.")
                showLimit = True
            else:
                break
        except:
            printSingleBar()
            print("You need to enter a number.")

    return number


# This function will make sure a name is valid
def checkName(name, length):
    if len(name) < 1:
        printSingleBar()
        print("Please enter a name.")
        printEmptySpace()
        return False
    elif name[0] == " ":
        printSingleBar()
        print("Your name can not begin with a space.")
        printEmptySpace()
        return False
    elif name[0] == "-":
        printSingleBar()
        print("Your name can not begin with a hyphen.")
        printEmptySpace()
        return False
    elif len(name) > length:
        printSingleBar()
        print("Your name is too long.")
        print("Please choose something")
        print("within " + str(length) + " characters.")
        printEmptySpace()
        return False
    else:
        for index in name:
            if not (index.isalnum() or index.isspace() or
                    index == "-"):
                printSingleBar()
                print("Please enter only letters, numbers,")
                print("spaces, and/or hyphens.")
                printEmptySpace()
                return False

    return True


def getRandomInt(beginning, end):
    return random.randint(beginning, end)


def printDoubleBar():
    print("==================================================")


def printSingleBar():
    print("--------------------------------------------------")


def printEmptySpace():
    print("")


main()
