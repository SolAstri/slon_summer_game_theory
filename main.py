from typing import Optional
import itertools
import random


class Prisoner:
    was_ratted_before: bool
    gamma: float
    score: float

    def __init__(self):
        self.was_ratted_before = False
        self.score = 0

    def turn(self, w_r_o_turn: bool = False):
        if w_r_o_turn:
            self.was_ratted_before = True

        print("Warning!")
        return False


class RatPrisoner(Prisoner):
    def turn(self, w_r_o_turn: bool = False):
        if w_r_o_turn:
            self.was_ratted_before = True
        return True


class ReverseRatPrisoner(Prisoner):
    def turn(self, w_r_o_turn: bool = False):
        if w_r_o_turn:
            self.was_ratted_before = True
        return False


class AvengerPrisoner(Prisoner):
    def turn(self, w_r_o_turn: bool = False):
        if w_r_o_turn or self.was_ratted_before:
            self.was_ratted_before = True
            return True
        return False


class BakaPrisoner(Prisoner):
    have_yelled: bool

    def __init__(self):
        super().__init__()
        self.have_yelled = False

    def turn(self, w_r_o_turn: bool = False):
        if not self.have_yelled:
            self.have_yelled = True
            return True
        else:
            return False


class ImitatorPrisoner(Prisoner):
    def turn(self, w_r_o_turn: bool = False):
        if w_r_o_turn:
            self.was_ratted_before = True
        return w_r_o_turn


class SmartGuyPrisoner(Prisoner):
    next_turn: str
    detected: Optional[str]
    det_pr: bool

    def __init__(self):
        super().__init__()
        self.next_turn = "first_a"
        self.detected = None
        self.det_pr = False

    def turn(self, w_r_o_turn: bool = False):
        if self.detected:
            if not self.det_pr:
                # print(f"Detected: {self.detected}")
                self.det_pr = True
            if (w_r_o_turn and (
                    self.detected == "reverse_rat" or
                    self.detected == "baka" or
                    self.detected == "imitator" or
                    self.detected == "smart_guy"
            )) \
                    or not w_r_o_turn and (self.detected == "avenger" or self.detected == "rat"):
                self.detected = "psycho"
                # print(f"Re-Detected: {self.detected}")
                self.next_turn = "psycho_strat"
                return True

        if self.next_turn == "first_a":
            self.next_turn = "first_b"
            return False

        if self.next_turn == "first_b":
            if w_r_o_turn:
                self.next_turn = "first_baka_or_rat"
                return True
            else:
                self.next_turn = "first_rait"
                return True

        # ----- #

        elif self.next_turn == "first_baka_or_rat":
            self.next_turn = "baka_rat_strat"
            if not w_r_o_turn:
                self.detected = "baka"
            else:
                self.detected = "rat"

            return True
        # ------ #

        elif self.next_turn == "first_rait":
            if w_r_o_turn:
                self.detected = "smart_guy"
                self.next_turn = "smart_guy_finale"
                return False
            else:
                self.next_turn = "first_rai"
                return False

        elif self.next_turn == "first_rai":
            if not w_r_o_turn:
                self.detected = "reverse_rat"
                self.next_turn = "rr_strat"
                return True
            else:
                self.next_turn = "first_ai"
                return False

        elif self.next_turn == "first_ai":
            if w_r_o_turn:
                self.detected = "avenger"
                self.next_turn = "avenger_strat"
                return True
            else:
                self.detected = "imitator"
                self.next_turn = "imitator_strat"
                return False

        # ------ #
        elif self.next_turn == "baka_rat_strat":
            return True

        elif self.next_turn == "rr_strat":
            return True

        elif self.next_turn == "avenger_strat":
            return True

        elif self.next_turn == "imitator_strat":
            return False

        elif self.next_turn == "psycho_strat":
            return True


class PsychoPrisoner(Prisoner):
    def turn(self, w_r_o_turn: bool = False):
        return True if random.random() > 0.5 else False


all_prisoners = [
    AvengerPrisoner, SmartGuyPrisoner, RatPrisoner,
    ReverseRatPrisoner, ImitatorPrisoner, PsychoPrisoner, BakaPrisoner
]

if __name__ == '__main__':
    combos = itertools.permutations(all_prisoners, r=2)

    result_table = [[0] * 8] * 8
    for i in range(1, len(result_table)):
        result_table[i][0] = all_prisoners[i - 1]

    for i in result_table:
        print(''.join(str(i)))

    position = [0, 0]

    for cmb in combos:
        position[1] += 1
        gamma = 0.9
        p_a = cmb[0]()
        p_b = cmb[1]()

        print(type(p_a).__name__, type(p_b).__name__)

        score_a = 0
        score_b = 0

        prev_a = p_a.turn(False)
        prev_b = p_b.turn(False)
        i_n = 10
        for i in range(i_n):
            position[0] += 1
            now_a = p_a.turn(prev_b)
            now_b = p_b.turn(prev_a)

            score_a += gamma * \
                       (1 if now_a and now_b else 2 if not now_a and not now_b else 4 if now_a and not now_b else 0)
            score_b += gamma * \
                       (1 if now_a and now_b else 2 if not now_a and not now_b else 4 if now_b and not now_a else 0)
            # print(i, now_a, now_b, gamma)
            prev_a = now_a
            prev_b = now_b

            gamma *= gamma

        print(score_a, score_b)