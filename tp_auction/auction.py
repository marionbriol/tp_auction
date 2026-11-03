# TODO !
from itertools import count

from utils import Cli

class Auction:

    def __init__(self, cli = None):
        self.cli = cli if cli else Cli()
        self.bidders = []
        self.standing_bid = None
        self.winner = None
        self.name = None


    def opening(self):
        self.cli.display(f"Started auction of type: {self.name}")
        opening_bid = self.cli.prompt('Please enter the amount for the opening bid:')
        opening_bid = int(opening_bid)
        self.cli.display(f"Opening bid is: {opening_bid}")
        self.standing_bid = opening_bid

    def bidders_init(self):
        for index in count(1):
            bidder = self.cli.prompt(f"Enter name for bidder {index} (enter nothing to move on):")
            if not bidder:
                break
            self.bidders.append(bidder)
        self.cli.display(f"\nBidders are: {', '.join(self.bidders)}\n")

    def winner_is(self):
        self.cli.display("\n~~~~~~~~\n")
        self.cli.display(f"Winner is {self.winner}. Winning bid is {self.standing_bid}.")

