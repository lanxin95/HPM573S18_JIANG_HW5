import numpy as np
import scr.SamplePathClass as SamplePathSupport
import scr.FigureSupport as FigSupport


class Game(object):
    def __init__(self, id, prob_head):
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin
        self._reward=-250
    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        self._reward = 100*self._countWins - 250
        return self._reward
    def loss(self):
        if self._reward < 0:
            lose_money = 1
        else:
            lose_money = 0
        return lose_money

class SetOfGames:
    def __init__(self, prob_head, n_games):
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._gameLoss = [] # create an empty list where loss will be stored
        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=prob_head)
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())
            self._gameLoss.append(game.loss())

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return sum(self._gameRewards) / len(self._gameRewards)

    def get_reward(self):
        return self._gameRewards

    def get_prob_loss(self):
        return sum(self._gameLoss) / len(self._gameLoss)

#Problem 1: Histogram of Rewards (Weight 1). Draw the histogram of rewards using 1,000 games with a fair coin.
# run trail of 1000 games to calculate expected reward
games = SetOfGames(prob_head=0.5, n_games=1000)
# print the average reward
print('Expected reward when the probability of head is 0.5:', games.get_ave_reward())
#What is the minimum and maximum reward that you expect to see when playing this game of chance?
print('Minimum reward:',min(games.get_reward()),'Maximum reward:',max(games.get_reward()))
#create histgram of game rewards
FigSupport.graph_histogram(games.get_reward(),title='Histogram',
                                    x_label='Game Rewards',y_label="Frequency")
#Problem 2: Probability of Loss (Weight 1).
print('Estimated probability of losing money when the probability of head is 0.5:', games.get_prob_loss())
