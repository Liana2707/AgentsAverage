import ast
import asyncio
from random import randint

from spade.behaviour import FSMBehaviour, State
from spade.message import Message

from Result import Result

STATE_ONE = "STATE_ONE SEND"
STATE_TWO = "STATE_TWO RECEIVE"
STATE_THREE = "STATE_TREE UPDATING SENDER"
STATE_FOUR = "STATE_FOUR CHECKING LEN(INFO)"
STATE_FIVE = "STATE FIVE FINISH"

SENDER_ID = 0
result = Result()


class SimpleBehaviour(FSMBehaviour):

    async def on_start(self):
        print(f"Initial {self.current_state} for {self.agent.jid}")

    async def on_end(self):
        await self.agent.stop()


class StateOne(State):
    async def run(self):
        self.agent.change_neighbours()
        for i in range(len(self.agent.neighbours)):
            print(f"SEND from {self.agent.jid} to agent{self.agent.neighbours[i]}@localhost")
            msg = Message()
            msg.to = f'agent{self.agent.neighbours[i]}@localhost'

            for agent in self.agent.info.keys(): # введение шумов
                noise = randint(-2, 2)
                self.agent.info[agent] += noise
            msg.body = f"{self.agent.info}"
            await asyncio.sleep(randint(0, 10)) #отправка с задержкой
            await self.send(msg)
            result.send_count += 1

        await asyncio.sleep(1)
        self.set_next_state(STATE_TWO)
        if self.agent.finished():
            self.set_next_state(STATE_FIVE)


class StateTwo(State):

    async def run(self):
        if self.agent.finished():
            self.set_next_state(STATE_FIVE)
        else:
            if SENDER_ID != self.agent.id:
                self.agent.change_neighbours()
                try:
                    msg = await self.receive(timeout=13) #  чтобы дождаться точной отправки
                    new_info = ast.literal_eval(msg.body)
                    
                    for agent in new_info.keys():
                        if agent not in self.agent.info.keys():
                            self.agent.info[agent] = new_info[agent]

                    for n in self.agent.neighbours:
                        try:
                            print(self.agent.jid, f"agent{n}@localhost")
                            self.agent.info[self.agent.jid] += (self.agent.info[f"agent{n}@localhost"] - new_info[self.agent.jid])/(1+self.agent.l)
                        except:
                            pass
                    # updating table info

                    print(f"received message {msg.body} for {self.agent.jid} from {msg.to}")
                except:
                    if SENDER_ID in self.agent.neighbours:
                        self.set_next_state(STATE_FIVE)
                    # выполняется если агент не является соседом отправителя
                    # или сообщение отправили на сервер

            self.set_next_state(STATE_THREE)


class StateThree(State):

    async def run(self):
        self.agent.change_neighbours()
        global SENDER_ID
        await asyncio.sleep(5)  # поздволяет дождаться момента,
        # когда все агенты завершат свою работу и сендер поменяется

        if self.agent.id == 0:
            SENDER_ID = SENDER_ID + 1 if SENDER_ID != 9 else 0
        self.set_next_state(STATE_FOUR)

        if self.agent.finished():
            self.set_next_state(STATE_FIVE)


class StateFour(State):
    async def run(self):
        global SENDER_ID
        self.agent.change_neighbours()
        if len(self.agent.info) < self.agent.number_of_agents:
            if SENDER_ID == self.agent.id:
                self.set_next_state(STATE_ONE)
            else:
                self.set_next_state(STATE_TWO)
        else:
            self.agent.__class__.finish = True

        if self.agent.finished():
            self.set_next_state(STATE_FIVE)


class StateFive(State):
    async def run(self):
        print("THATS RED BUTTON")
        await asyncio.sleep(7)
        if result.value == 0 and len(self.agent.info) == self.agent.number_of_agents:
            for agent in self.agent.info.keys():
                result.plus_count += 1
                result.value += self.agent.info[agent]
            result.multiply_count += 1
            result.value /= self.agent.number_of_agents
            print("result = ", result.value)
            result.show(self.agent.info)
