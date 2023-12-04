import ast
import asyncio

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
        for i in range(len(self.agent.neighbours)):
            print(f"SEND from {self.agent.jid} to agent{self.agent.neighbours[i]}@localhost")
            msg = Message()
            msg.to = f'agent{self.agent.neighbours[i]}@localhost'
            msg.body = f"{self.agent.info}"
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
                try:
                    msg = await self.receive(timeout=3)
                    self.agent.info.update(ast.literal_eval(msg.body))  # updating table info
                    print(f"received message {msg.body} for {self.agent.jid} from {msg.to}")
                except:
                    if SENDER_ID in self.agent.neighbours:
                        self.set_next_state(STATE_FIVE)
                    # выполняется если агент не является соседом отправителя
                    # или сообщение отправили на сервер

            self.set_next_state(STATE_THREE)


class StateThree(State):

    async def run(self):
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
            print(result.value)
            result.show(self.agent.info)
