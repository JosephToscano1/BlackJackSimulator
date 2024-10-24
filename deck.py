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
class cardShoe:
    def __init__(self, decks, cutDealt):
        self.decks = decks
        self.cutDealt = cutDealt

# @param int decks - number of decks
# @return shoe comprised of given number of decks
def buildDeck(shuffledShoe, decks):

    #Template deck of strings representing a 52 card deck of cards

    deck = ["2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "Js", "Qs", "Ks", "As",
            "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "Jh", "Qh", "Kh", "Ah",
            "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "Jd", "Qd", "Kd", "Ad",
            "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "Jc", "Qc", "Kc", "Ac"]
    currShoe = []

    #Make current shoe by putting together mutiple decks
    for i in range(decks):
        currShoe += deck

    #Shuffle the shoe by randomly popping elements from current shoe and adding them to new list (not replicative of human shuffling for now)

    for x in range(len(currShoe)):
        if(len(currShoe) == 1):
            shuffledShoe.decks.append(currShoe.pop(0))
            currShoe = deck
        else:
            shuffledShoe.decks.append(currShoe.pop(random.randint(0, len(currShoe)-1)))

    # Insert cut card at a random spot around 1-1.5 decks in
    shuffledShoe.decks.insert(random.randint(47, 83), "CUTc")

    return shuffledShoe

# @param shoe, dealer to be dealt cards
# deal a card to the dealer and update total
def dealToDealer(shoe, dlr):
    dlr.hand.append(shoe.decks.pop(0))
    currCard = dlr.hand[len(dlr.hand)-1][: -1]
    if(currCard == "CUT"):
        dlr.hand.pop(len(dlr.hand)-1)
        shoe.cutDealt = True
        dealToDealer(shoe, dlr)
    else:
        if(currCard.isnumeric()):
            dlr.handTotal += int(currCard)
        elif(currCard == 'A'):
            if(dlr.handTotal + 11 < 22):
                dlr.handTotal +=  11
                dlr.highAce = True
            else:
                dlr.handTotal += 1
        else:
            dlr.handTotal += 10

# deal a card to the hand provided and update its total
def dealToPlayer(shoe, player, handNo):
    
    player.hands[handNo].append(shoe.decks.pop(0))
    currCard = player.hands[handNo][len(player.hands[handNo])-1][: -1]

    # If cut card is reached, take note of it and continue dealing like normal
    if(currCard == "CUT"):
        player.hands[handNo].pop(len(player.hands[handNo])-1)
        shoe.cutDealt = True
        dealToPlayer(shoe, player, handNo)
    else:
        # If the card is a number, add it to total, if ace add either 1 or 11, face add 10
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
        # check if a hand won, tied, or lost and update player's balance accordingly
        for j in range(len(plrs[i].hands)):
            if(plrs[i].handTotals[j] == 21 and len(plrs[i].hands[j]) == 2):
                plrs[i].balance += plrs[i].bets[j]*2
                plrs[i].balance += plrs[i].bets[j]/2
                print("Player "+ str(i+1) +" wins with Blackjack on hand "+str(j+1)+"!")
            elif(plrs[i].handTotals[j] < 22 and ((plrs[i].handTotals[j] > dlr.handTotal) or (dlr.handTotal > 21))):
                plrs[i].balance += plrs[i].bets[j]*2
                print("Player "+ str(i+1)+ " wins on hand "+str(j+1)+"!")
            elif(plrs[i].handTotals[j] == dlr.handTotal and plrs[i].handTotals[j] < 22):
                plrs[i].balance += plrs[i].bets[j]
                print("Player " + str(i + 1) + " push on hand " + str(j + 1) + ", eh")
            else:
                print("Player " + str(i + 1) + " loses on hand "+str(j+1)+" :( ")
        print("Balance: " + str(plrs[i].balance))
    # reset initial values for player and dealer attributes
    for x in range(len(plrs)):
        plrs[x].hands = []
        plrs[x].highAce = []
        plrs[x].insurance = False
        plrs[x].handTotals = []
        plrs[x].bets = []
    dlr.hand = []
    dlr.handTotal = 0
    dlr.highAce = False    

# evaluate dealer's turn (draw until H17, default rules are S17)
def dlrTurn(shoe, dlr, Hit17):
    while(dlr.handTotal<17):
        dealToDealer(shoe, dlr)
        if(dlr.handTotal > 21 and dlr.highAce):
            dlr.handTotal -= 10
            dlr.highAce = False
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
        action = input("Player "+str(plrNo)+": Given hand "+ str(handNo + 1)+", would you like to hit, stand, split, surrender, or double? (type h, st, sp, su, or d): ")

        # If a player has two of the same cards, allow them to split them into two hands
        if(action == "sp"):
            if(plr.bets[handNo] > plr.balance):
                print("Insufficient balance to split")
                initialPlayerOptions(plrNo, plr, handNo, shoe)
            else:
                card1 = plr.hands[handNo][0][: -1]
                card2 = plr.hands[handNo][1][: -1]
                if(card1 == card2):
                    # add new hand to the player that is splitting
                    plr.hands.insert(handNo, [plr.hands[handNo].pop(1)])
                    plr.handTotals.insert(handNo, 0)

                    # split hand total accross the two new hands by subtracting second card value from old total and adding it to new one
                    if(card2.isnumeric()):
                        # number card
                        plr.handTotals[handNo+1] -= int(card2)
                        plr.handTotals[handNo] += int(card2)
                    elif(card2 == 'A'):
                        # ace
                        plr.handTotals[handNo+1] -= 11
                        plr.handTotals[handNo] += 11
                    else:
                        # face card
                        plr.handTotals[handNo+1] -= 10
                        plr.handTotals[handNo] += 10
                    
                    # adjust player bets and balance accordingly

                    plr.bets.insert(handNo, plr.bets[handNo])
                    plr.balance -= plr.bets[handNo]
                    
                    # deal to each new hand and print

                    dealToPlayer(shoe, plr, handNo)
                    dealToPlayer(shoe, plr, handNo+1)
                    print("Player " + str(plrNo) + "\n New Hand " + str(handNo + 1) + ": " + str(
                        plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
                    print("Player " + str(plrNo) + "\n New Hand " + str(handNo + 2) + ": " + str(
                        plr.hands[handNo+1]) + "\n Total: " + str(plr.handTotals[handNo+1]) + "\n")
                    
                    # If a pair of aces was split and the next card to a new hand is not an ace, player cannot act on the hand
                    if(not((card1 == 'A' and card2 != 'A') or (card2 == 'A' and card1 != 'A'))):
                        initialPlayerOptions(plrNo, plr, handNo, shoe)
                    if(not((card1 == 'A' and card2 != 'A') or (card2 == 'A' and card1 != 'A'))):
                        initialPlayerOptions(plrNo, plr, handNo+1, shoe)
                else:
                    print("Sorry, you may only split when you have a pair of same-value cards")
                    initialPlayerOptions(plrNo, plr, handNo, shoe)

        # hit, deal a card to the player and update total. If the player did not bust, send to further actions
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

        # double, subtract player bet again from total and adjust it. Deal one more card to player ending their turn.
        if(action == "d"):
            if(plr.bets[handNo] > plr.balance):
                print("Insufficient balance to double")
                initialPlayerOptions(plrNo, plr, handNo, shoe)
            else:
                if (plr.handTotals[handNo] > 21):
                    if (plr.highAce[handNo]):
                        plr.handTotals[handNo] -= 10
                plr.balance -= plr.bets[handNo]
                plr.bets[handNo] += plr.bets[handNo]
                dealToPlayer(shoe, plr, handNo)
                print("Player " + str(plrNo) + "\n Balance: " + str(plr.balance) + "\n Hand "+ str(handNo + 1)+": " + str(plr.hands[handNo]) + "\n Total: " + str(plr.handTotals[handNo]) + "\n")
        
        # surrender, give player half of their bet back, remove the hand, and end their turn
        if(action == "su"):
            plr.balance += plr.bets[handNo]/2
            plr.hands.pop(handNo)
            print("Hand "+ str(handNo + 1) + " surrendered. \n Balance: "+ str(plr.balance))

# deal hands to each player and the dealer
def initialDeal(shoe, plrs, plrCount, first, decks, Hit17):
    dlrAce = False
    enteredCount = False
    enteredBet = False

    # If this is the first deal, get player balance and burn the first card, regardless, get number of hands and set default values for each player
    if(first):
        for x in range(plrCount):
            plrs.append(player(int(input("Player "+ str(x +1)+", how much of the college fund are we playing with today? ")),
                               [],
                               [], [], [], False))
        #Burn first card
        shoe.decks.pop(0)
        first = False

    enteredCount = False
    # For each player, check if they have a sufficient balance. If so, proceed, if not remove player
    for x in range(plrCount):
        if(plrs[x].balance < 10):
            plrs.pop(x)
            print("Player "+str(x+1)+" has been removed due to insufficient balance. Player numbers have shifted accordingly")
        else:
            # progress when player enters a valid hand count
            while(not(enteredCount)):
                handCount = int(input("Player "+str(x+1)+", how many hands are you playing with? "))
                if(handCount > 3 or handCount < 1):
                    print("Apologies, each player must have at least 1 and no more than 3 hands")
                else:
                    enteredCount = True
            # progress when player enters a valid bet
            for y in range(handCount):
                enteredBet = False
                while(not(enteredBet)):
                    bet = int(input("Player " + str(x + 1) + ", place your bet for hand " + str(y + 1) + ": "))
                    if(bet > plrs[x].balance):
                        print("Insufficient balance for bet")
                    else:
                        enteredBet = True

                # set player variables for current hand
                plrs[x].bets.append(bet)
                plrs[x].hands.append([])
                plrs[x].balance -= plrs[x].bets[y]
                plrs[x].highAce.append(0)
                plrs[x].handTotals.append(0)

    dlr = dealer(0, [], False)

    # Deal two cards to each player and dealer, show dealer up card
    for y in range(2):
        for i in range(plrCount):
            for j in range(len(plrs[i].hands)):
                dealToPlayer(shoe, plrs[i], j)
        if(len(dlr.hand) == 0):
            dealToDealer(shoe, dlr)
            upCard = dlr.hand[0]
            print("\nDealer's up card: "+ upCard + "\n")
        else:
            dealToDealer(shoe, dlr)

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

    # Resolve game early if dealer has blackjack, else proceed to initial options for each player hand
    if (dlr.handTotal == 21):
        print("Dealer has Blackjack")
        for i in range(plrCount):
            for j in range(len(plrs[i].hands)):
                # Check if any players also have blackjack
                if(plrs[i].handTotals[j] == 21):
                    plrs[i].balance += plrs[i].bets[j]
                    print("Player "+ str(i+1)+" push on hand "+str(j+1))
                # Check if dealer had ace showing and that players bought insurance
                elif(plrs[i].insurance and dlrAce):
                    plrs[i].balance += plrs[i].bets[j]*2
                    print("Player "+ str(i+1)+" cashes insurace on hand "+str(j+1))
        cleanup(plrs, dlr)
    else:
        for i in range(plrCount):
            for j in range(len(plrs[i].hands)):
                initialPlayerOptions(i+1, plrs[i], j, shoe)
        dlrTurn(shoe, dlr, Hit17)
        cleanup(plrs, dlr)
    if(shoe.cutDealt):
        print("Cut card dealt, reshuffling shoe")
        shoe = cardShoe([], False)
        buildDeck(shoe, decks)
    initialDeal(shoe, plrs, plrCount, first, decks, Hit17)

# get number of decks in the shoe and players
def main():

    decks = int(input("\nWelcome to the Blackjack table, now let's go gambling! How many decks do you want to play with? "))
    shoe = cardShoe([], False)
    buildDeck(shoe, decks)
    Hit17 = int(input("What ruleset should be played? Type 1 to play dealer must hit soft 17. Type 0 to play dealer must stand on soft 17: "))
    plrCount = int(input("And how many of us have the winning mentality? "))
    if(plrCount > 7 or plrCount < 1):
        print("I'm sorry, Blackjack may only be played with at least 1 player and no more than 7")
        main()
    print("Excellent.\n")
    initialDeal(shoe, [], plrCount, True, decks, Hit17)

main()