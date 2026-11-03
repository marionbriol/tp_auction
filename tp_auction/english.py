# pylint: disable=missing-docstring
from itertools import count

from utils import Cli

from auction import Auction

class EnglishAuction(Auction):

    def __init__(self, cli=None):
        super().__init__(cli)
        self.auction_name = "English"

    def name(self):
        return self.auction_name

    def play(self):
        B = True
        super().opening
        super().bidders_init

        while B:
            B = False
            for bidder in self.bidders:
                bid = self.cli.prompt(f"Standing bid is {self.standing_bid}. {bidder} bids:")
                if not bid:
                    continue
                else:
                    bid=int(bid)
                    B = True
                    if bid > self.standing_bid:
                        self.standing_bid = bid
                        self.winner = bidder

        super().winner_is




if __name__ == "__main__":
    auction = EnglishAuction()
    auction.play()

