import random

#imports and global variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
             'Queen':10, 'King':10, 'Ace':11}


playing = True


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return f'{self.rank} of {self.suit}'


#this class holds deck of 52 cards and methods
class Deck:
    def __init__(self):
        self.deck = []
        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(suit, rank))
                
    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        return self.deck.pop()
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        #value is the total number of cards
        
        if card.rank == 'Ace':
            self.aces +=1
        
    def adjust_for_ace(self):
        while self.value > 21 and self.aces: 
            self.value -=10
            self.aces -=1


class Chips:
    def __init__(self, total =100):
        self.total = total
        self.bet = 0
        
    def win_bet(self):
        self.total+=self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        
        try:
            chips.bet = int(input('how many chips would you like to bet: '))
        except:
            print("sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print("sorry you do not have enough chips")
            else:
                break  

def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing 

    while True:
        x = input("hit or stand?: enter 'h' or 's'")
        
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print('player stands dealers turn')
            playing = False
        else: 
            print("sorry I did not understand that, please enter 'h' or 's' only")
            continue
        
        break



def show_some(player, dealer):
    #show only one of the dealers cards
    print("\n dealer's hand: ")
    print("first card hidden!")
    print(dealer.cards[1])
    
    #show all the 2 cards of the player's hand
    print("\n player's hand: ")
    for card in player.cards:
        print(card)

def show_all(player, dealer):
    #show all the 2 cards of the player's hand
    print("\n Dealer's hand: ")
    
    for card in dealer.cards:
        print(card)
        
    #alternative way of printing all the items in a list without a for loop
    #print("the dealers cards is: "*dealer.cards,sep='\n')
        
    #calculate and display the value of the cards in the dealers hand
    print(f"value of dealers hand is: {dealer.value}")
    
    #show all the 2 cards of the player's hand
    print("\n player's hand: ")
    for card in player.cards:
        print(card)
    print(f"value of dealers hand is: {dealer.value}")


#functions to handle end game scenarios
def player_busts(player, dealer, chips):
    print('BUST PLAYER!')
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print('PLAYER WINS')
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print('PLAYER WINS, DEALER BUSTED!')
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print('DEALER WINs!')
    chips.lose_bet()

def push(player, dealer):
    print("dealer and player tie! PUSH")


while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #set up player chips
    player_chips = Chips()
    take_bet(player_chips)
    
    #show some of the card
    show_some(player_hand, dealer_hand)
    
    while playing:
        hit_or_stand(deck, player_hand)
        
        show_some(player_hand, dealer_hand)
        
        #if player hand exceeds 21 run player_busts and break out of the loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
        
    if player_hand.value <= 21:
        
        while dealer_hand.value < player_hand.value:
            hit(deck, dealer_hand)
        
        #show all cards
        show_all(player_hand, dealer_hand)
        
        #run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    print('\n player total chips are at: {}'.format(player_chips.total))
    
     # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower()=='y':
        playing=True
        continue
    else:
        print("Thanks for playing!")
        break