

class Result:
    send_on_server_value = 1000
    send_value = 1
    plus_value = 0.01
    multiply_value = 0.1
    memory_value = 1

    send_on_server_count = 1.
    send_count = 0.
    plus_count = 0.
    multiply_count = 1.
    memory_count = 10.

    value = 0

    def show(self, info):
        print('________________________________________')
        for agent in info.keys():
            print(agent, info[agent])

        cost = (self.send_on_server_value * self.send_on_server_count +
                self.send_value * self.send_count +
                self.plus_value * self.plus_count +
                self.multiply_value * self.multiply_count +
                self.memory_value * self.memory_count)

        print(f"cost = {cost}")



