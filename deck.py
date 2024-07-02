import random

class player:
    def __init__(self, balance, bets, handTotals, highAce, hands, insurance):
        self.balance = balance
        self.bets = bets
        self.handTotals = handTotals
        self.highAce = highAce
        self.hands = hands
        self.insurance = insurance

class dealer:
    def __init__(self, handTotal, hand, highAce):
        self.handTotal = handTotal
        self.hand = hand
        self.highAce = highAce

# @param int decks - number of decks
# @return shoe comprised of given number of decks
def buildDeck(decks):

    #Template deck of strings representing a 52 card deck of cards

    deck = ["2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As",
            "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
            "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
            "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac"]
    shuffledShoe = []
    currShoe = []

    #Make current shoe by putting together mutiple decks
    for i in range(decks):
        currShoe += deck

    #Shuffle the shoe by randomly popping elements from current shoe and adding them to new list (not replicative of human shuffling for now)

    for x in range(len(currShoe)):
        if(len(currShoe) == 1):
            shuffledShoe.append(currShoe.pop(0))
            currShoe = deck
        else:
            shuffledShoe.append(currShoe.pop(random.randint(0, len(currShoe)-1)))
    return shuffledShoe

# @param shoe, player to be dealt cards
# deal a card to a player's hand and update total
def dealToDealer(shoe, player):
    player.hand.append(shoe.pop(0))
    currCard = player.hand[len(player.hand)-1][: -1]
    if(currCard.isnumeric()):
        player.handTotal += int(currCard)
    elif(currCard == 'A'):
        if(player.handTotal + 11 < 22):
            player.handTotal +=  11
            player.highAce = True
        else:
            player.handTotal += 1
    else:
        player.handTotal += 10

def dealToPlayer(shoe, player, handNo):
    player.hands[handNo].append(shoe.pop(0))
    currCard = player.hands[handNo][len(player.hands[handNo])-1][: -1]
    if(currCard.isnumeric()):
        player.handTotals[handNo] += int(currCard)
    elif(currCard == 'A'):
        if(player.handTotals[handNo] + 11 < 22):
            player.handTotals[handNo] +=  11
            player.highAce[handNo] = 1
        else:
            player.handTotals[handNo] += 1
    else:
        player.handTotals[handNo] += 10

# reset hands, totals, and variables of player and dealer.
def cleanup(plrs, dlr):
    for i in range(len(plrs)):
        for j in range(len(plrs[i].hands)):
            if(plrs[i].handTotals[j] == 21 and dlr.handTotal != 21):
                plrs[i].balance += plrs[i].bets[j]*3
                print("Player "+ str(i+1) +" wins with Blackjack on hand "+str(j+1)+"!")
            elif(plrs[i].handTotals[j] < 21 and ((plrs[i].handTotals[j] > dlr.handTotal) or (dlr.handTotal > 21))):
                plrs[i].balance += plrs[i].bets[j]*2
                print("Player "+ str(i+1)+ " wins on hand "+str(j+1)+"!")
            elif(plrs[i].handTotals[j] == dlr.handTotal):
                plrs[i].balance += plrs[i].bets[j]
                print("Player " + str(i + 1) + " push on hand " + str(j + 1) + ", eh")
            else:
                print("Player " + str(i + 1) + " loses on hand "+str(j+1)+" :( ")
        print("Balance: " + str(plrs[i].balance))
    for x in range(len(plrs)):
        plrs[x].hands = []
        plrs[x].highAce = []
        plrs[x].insurance = False
        plrs[x].handTotals = []
    dlr.hand = []
    dlr.handTotal = 0;
    dlr.highAce = False

# evaluate dealer's turn (draw until H17)
def dlrTurn(shoe, dlr):
    while(dlr.handTotal<17):
        dealToDealer(shoe, dlr)
        if(dlr.handTotal > 21 and dlr.highAce):
            dlr.handTotal -= 10
    print("Dealer hand after drawing cards:" + str(dlr.hand))
    print("Total: "+ str(dlr.handTotal))

# give the current player options after drawing their first card if they are still active (hit or stand)
def furtherPlayerOptions(plrNo, plr, handNo, shoe):
    action = action = input("Player "+str(plrNo)+": Given hand "+ str(handNo + 1)+", would you like to hit or stand? (type h or st): ")
    if (action == "h"):
        dealToPlayer(shoe, plr, handNo)
        if (plr.handTotals[handNo] > 21):
            if (plr.highAce[handNo]):
                plr.handTotals[handNo] -= 10
                plr.highAce[handNo] = 0
                print("Player " + str(plrNo) + "\n Hand " + str(handNo + 1) + ": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
                furtherPlayerOptions(plrNo, plr, handNo, shoe)
            else:
                print("Player " + str(plrNo) + "\n Hand "+ str(handNo+1)+": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
                print("Player " + str(plrNo) + " has busted all over the table")
        else:
            print("Player " + str(plrNo) + "\n Hand "+ str(handNo+1)+": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
            furtherPlayerOptions(plrNo, plr, handNo, shoe)

# Give player their full intial options: hit, stand, double, or split if they have a pair
def initialPlayerOptions(plrNo, plr, handNo, shoe):
    # player template [money, current bet, total, Ace?, card1, card2]
    # dealer hand [total, card1 (up card), card2]
    if(plr.handTotals[handNo] != 21):
        action = input("Player "+str(plrNo)+": Given hand "+ str(handNo + 1)+", would you like to hit, stand, split, or double? (type h, st, sp, or d): ")


        if(action == "sp"):
            card1 = plr.hands[handNo][0][: -1]
            card2 = plr.hands[handNo][1][: -1]
            if(card1 == card2):
                plr.hands.insert(handNo, [plr.hands[handNo].pop(1)])
                plr.handTotals.insert(handNo, 0)
                if(card2.isnumeric()):
                    plr.handTotals[handNo+1] -= int(card2)
                    plr.handTotals[handNo] += int(card2)
                elif(card2 == 'A'):
                    plr.handTotals[handNo+1] -= 11
                    plr.handTotals[handNo] += 11
                else:
                    plr.handTotals[handNo+1] -= 10
                    plr.handTotals[handNo] += 10
                plr.bets.insert(handNo, plr.bets[handNo])
                plr.balance -= plr.bets[handNo]
                dealToPlayer(shoe, plr, handNo)
                dealToPlayer(shoe, plr, handNo+1)
                print("Player " + str(plrNo) + "\n New Hand " + str(handNo + 1) + ": " + str(
                    plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
                print("Player " + str(plrNo) + "\n New Hand " + str(handNo + 2) + ": " + str(
                    plr.hands[handNo+1]) + "\n Total: " + str(plr.handTotals[handNo+1]) + "\n")
                if(not((plr.hands[handNo][0][: -1] == 'A' and plr.hands[handNo][1][: -1] != 'A') or (plr.hands[handNo][1][: -1] == 'A' and plr.hands[handNo][0][: -1] != 'A'))):
                    initialPlayerOptions(plrNo, plr, handNo, shoe)
                if(not((plr.hands[handNo][0][: -1] == 'A' and plr.hands[handNo][1][: -1] != 'A') or (plr.hands[handNo][1][: -1] == 'A' and plr.hands[handNo][0][: -1] != 'A'))):
                    initialPlayerOptions(plrNo, plr, handNo+1, shoe)
            else:
                print("Sorry, you may only split when you have a pair of same-value cards")
                initialPlayerOptions(plrNo, plr, handNo, shoe)

        if(action == "h"):
            dealToPlayer(shoe, plr, handNo)
            if(plr.handTotals[handNo] > 21):
                if(plr.highAce[handNo]):
                    plr.handTotals[handNo] -= 10
                    plr.highAce[handNo] = 0
                    print("Player " + str(plrNo) + "\n Hand " + str(handNo + 1) + ": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
                    furtherPlayerOptions(plrNo, plr, handNo, shoe)
                else:
                    print("Player " + str(plrNo) + "\n Hand "+ str(handNo + 1)+": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
                    print("Player " + str(plrNo) + " has busted all over the table")
            else:
                print("Player " + str(plrNo) + "\n Hand "+ str(handNo + 1)+": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
                furtherPlayerOptions(plrNo, plr, handNo, shoe)
        if(action == "d"):
            plr.balance -= plr.bets[handNo]
            plr.bets[handNo] += plr.bets[handNo]
            dealToPlayer(shoe, plr, handNo)
            print("Player " + str(plrNo) + "\n Balance: " + str(plr.balance) + "\n Hand "+ str(handNo + 1)+": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")

# deal hands to each player and the dealer
def initialDeal(shoe, plrs, plrCount, first):
    dlrAce = False

    # For each player, populate their balance, bet, and placeholders
    if(first):
        for x in range(plrCount):
            plrs.append(player(int(input("Player "+ str(x +1)+", how much of the college fund are we playing with today? ")),
                               [],
                               [], [], [], False))
            for y in range(int(input("And how many hands are you playing with? "))):
                plrs[x].bets.append(int(input("Player " + str(x + 1) + ", place your bet for hand "+ str(y+1)+ ": ")))
                plrs[x].hands.append([])
                plrs[x].balance -= plrs[x].bets[y]
                plrs[x].highAce.append(0)
                plrs[x].handTotals.append(0)
        #Burn first card
        shoe.pop(0)
        first = False
    else:
        for x in range(plrCount):
            for y in range(int(input("Player "+ str(x+1) +", how many hands are you playing with? "))):
                plrs[x].bets.append(int(input("Player " + str(x + 1) + ", place your bet for hand " + str(y + 1) + ": ")))
                plrs[x].hands.append([])
                plrs[x].balance -= plrs[x].bets[y]
                plrs[x].highAce.append(0)
                plrs[x].handTotals.append(0)

    dlr = dealer(0, [], False)

    # Deal two cards to each player and dealer, show dealer up card
    for y in range(2):
        for i in range(plrCount):
            for j in range(len(plrs[i].hands)):
                plrs[i].hands[j].append(shoe.pop(0))
        if(len(dlr.hand) == 0):
            upCard = shoe.pop(0)
            dlr.hand.append(upCard)
            print("\nDealer's up card: "+ upCard + "\n")
        else:
            dlr.hand.append(shoe.pop(0))

    # Calculate total hand value for each player, then display hand and total value
    for i in range(plrCount):
        for j in range(len(plrs[i].hands)):
            for k in range(len(plrs[i].hands[j])):
                currCard = plrs[i].hands[j][k][: -1]
                if(currCard.isnumeric()):
                    plrs[i].handTotals[j] += int(currCard)
                elif(currCard == 'A'):
                    if(plrs[i].handTotals[j] + 11 < 22):
                        plrs[i].handTotals[j] +=  11
                        plrs[i].highAce[j] = 1
                    else:
                        plrs[i].handTotals[j] += 1
                else:
                    plrs[i].handTotals[j] += 10

    # Calculate dealer hand total
    for i in range(len(dlr.hand)):
        currCard = dlr.hand[i][: -1]
        if (currCard.isnumeric()):
            dlr.handTotal += int(currCard)
        elif (currCard == 'A'):
            if (dlr.handTotal + 11 < 22):
                dlr.handTotal += 11
                dlr.highAce = True
            else:
                dlr.handTotal += 1
        else:
            dlr.handTotal += 10

    # Display balance and hands for each player
    for i in range(plrCount):
        print("Player "+ str(i+1) + "\n Balance: "+ str(plrs[i].balance))
        for j in range(len(plrs[i].hands)):
            print("\n Hand "+ str(j+1) +": "+ str(plrs[i].hands[j]) + "\n Total: "+ str(plrs[i].handTotals[j])+"\n")

    # Check if dealer has ace, if so prompt each player on buying insurance
    if (dlr.hand[0][: -1] == 'A'):
        dlrAce = True
        for i in range(plrCount):
            answer = input("Player "+ str(i+1) +", would you like to buy insurance? (Y/N)")
        if (answer == "Y"):
            for j in range(len(plrs[i].hands)):
                plrs[i].balance -= plrs[i].bets[j] / 2
                plrs[i].insurance = True

    # Resolve game early if dealer has blackjack
    if (dlr.handTotal == 21):
        print("Dealer has Blackjack")
        for i in range(plrCount):
            for j in range(len(plrs[i].hands)):
                if(plrs[i].handTotals[j] == 21):
                    plrs[i].balance += plrs[i].bets[j]
                    print("Player "+ str(i+1)+" push on hand "+str(j+1))
                elif(plrs[i].insurance and dlrAce):
                    plrs[i].balance += plrs[i].bet*2
                    print("Player "+ str(i+1)+" cashes insurace on hand "+str(j+1))
        cleanup(plrs, dlr)
    else:
        for i in range(plrCount):
            for j in range(len(plrs[i].hands)):
                initialPlayerOptions(i+1, plrs[i], j, shoe)
        dlrTurn(shoe, dlr)
        cleanup(plrs, dlr)
    initialDeal(shoe, plrs, plrCount, first)

# get number of decks in the shoe and players
def main():
    decks = int(input("Welcome to the Blackjack table, now let's go gambling! How many decks do you want to play with? "))
    shoe = buildDeck(decks)
    plrCount = int(input("And how many of us have the winning mentality? "))
    print("Excellent.\n")
    initialDeal(shoe, [], plrCount, True)
main()