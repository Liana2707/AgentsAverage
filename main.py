import spade

from SimpleAgent import SimpleAgent


async def main():
    agents = [SimpleAgent(f'agent{i}@localhost', "123") for i in range(10)]
    for i in range(10):
        await agents[i].start()

    print("Agents started")
    for i in range(10):
        await spade.wait_until_finished(agents[i])

    for i in range(10):
        await agents[i].stop()
    print("Agents finished")


if __name__ == "__main__":
    spade.run(main())
