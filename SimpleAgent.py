import random
from random import randint

from spade.agent import Agent

from SimpleBehaviour import (
    SimpleBehaviour,
    STATE_ONE, STATE_TWO, STATE_THREE, STATE_FOUR, STATE_FIVE,
    StateOne, StateTwo, StateThree, StateFour,  StateFive
)

COUNT_AGENTS = 0

connections = [
    [1, 2, 3, 7],
    [0, 6],
    [0, 4, 5],
    [0, 4, 7, 8],
    [2, 3, 5, 8],
    [2, 6, 4],
    [1, 5, 9],
    [0, 3],
    [4, 3, 9],
    [8]
]

class SimpleAgent(Agent):
    number_of_agents = 10
    finish = False

    def __init__(self, jid: str, password: str):
        global COUNT_AGENTS
        self.id = COUNT_AGENTS
        COUNT_AGENTS += 1
        self.neighbours = connections[self.id]
        self.l = len(self.neighbours)
        self.value = 10
        self.number = self.value
        self.info = {jid: self.number}

        super().__init__(jid, password)

    def set_number_of_agents(self, number_of_agents, new_neighbours):
        self.number_of_agents = number_of_agents
        self.neighbours += new_neighbours

    def finished(self):
        return self.finish

    def change_neighbours(self):
        is_change = random.choice([True, False])
        if is_change:
            if self.id == 0:
                if 2 in self.neighbours:
                    self.neighbours.remove(2)
                else:
                    self.neighbours.append(2)
            elif self.id == 1:
                if 6 in self.neighbours:
                    self.neighbours.remove(6)
                else:
                    self.neighbours.append(6)
            elif self.id == 3:
                if 7 in self.neighbours:
                    self.neighbours.remove(7)
                else:
                    self.neighbours.append(7)
            elif self.id == 8:
                if 9 in self.neighbours:
                    self.neighbours.remove(9)
                else:
                    self.neighbours.append(9)


    async def setup(self):
        behaviour = SimpleBehaviour()

        behaviour.add_state(name=STATE_ONE, state=StateOne())
        behaviour.add_state(name=STATE_TWO, state=StateTwo(), initial=True)
        behaviour.add_state(name=STATE_THREE, state=StateThree())
        behaviour.add_state(name=STATE_FOUR, state=StateFour())
        behaviour.add_state(name=STATE_FIVE, state=StateFive())

        behaviour.add_transition(source=STATE_ONE, dest=STATE_TWO)
        behaviour.add_transition(source=STATE_ONE, dest=STATE_FIVE)

        behaviour.add_transition(source=STATE_TWO, dest=STATE_THREE)
        behaviour.add_transition(source=STATE_TWO, dest=STATE_FIVE)

        behaviour.add_transition(source=STATE_THREE, dest=STATE_FOUR)
        behaviour.add_transition(source=STATE_THREE, dest=STATE_FIVE)

        behaviour.add_transition(source=STATE_FOUR, dest=STATE_ONE)
        behaviour.add_transition(source=STATE_FOUR, dest=STATE_TWO)
        behaviour.add_transition(source=STATE_FOUR, dest=STATE_FIVE)

        self.add_behaviour(behaviour)
