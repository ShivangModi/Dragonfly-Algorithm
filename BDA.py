import random


# Define the Job class
class Job:
    def __init__(self, tasks, due_date):
        self.tasks = tasks
        self.due_date = due_date


# Define the Machine class
class Machine:
    def __init__(self, processing_times):
        self.processing_times = processing_times


# Define the Dragonfly class
class Dragonfly:
    def __init__(self, schedule):
        self.schedule = schedule
        self.fitness = 0

    # def mutate(self, machines):
    #     for i in range(len(self.schedule)):
    #         if random.random() < 0.1:
    #             self.schedule[i] = random.sample(range(len(machines)), len(self.schedule[i]))

    def evaluate(self, job, machine):
        makespan, tardiness = 0, 0
        for j in job:
            completion_time = 0
            for task in j.tasks:
                m = machine[task[0]]
                processing_time = m.processing_times[task[1]]
                completion_time += processing_time
            makespan = max(makespan, completion_time)
            tardiness += max(0, completion_time - j.due_date)
        self.fitness = (makespan, makespan + tardiness)


# Define the function to solve the flexible job-shop scheduling problem
class DragonFlyAlgorithm:
    @staticmethod
    def bda(job, machine, num_dragonflies, num_iterations):
        # Initialize the population of dragonflies
        population = list()
        for i in range(num_dragonflies):
            schedule = list()
            for j in job:
                schedule.append(random.sample(range(len(machine)), len(j.tasks)))
            dragonfly = Dragonfly(schedule)
            population.append(dragonfly)

        # Run the basic Dragonfly algorithm
        for i in range(num_iterations):
            for dragonfly in population:
                dragonfly.evaluate(job, machine)
            population.sort(key=lambda x: x.fitness[0])
            population = population[:50]

        # Return the best schedule
        return population[0]

    @staticmethod
    def moda(job, machine, num_dragonflies, num_iterations):
        # Initialize population of dragonflies randomly
        population = list()
        for i in range(num_dragonflies):
            schedule = list()
            for j in job:
                schedule.append(random.sample(range(len(machine)), len(j.tasks)))
            dragonfly = Dragonfly(schedule)
            dragonfly.evaluate(job, machine)
            population.append(dragonfly)

        # Run MODA algorithm
        for _ in range(num_iterations):
            # Sort dragonflies in non-ascending order based on fitness
            population.sort(key=lambda x: x.fitness[1], reverse=True)

            # Select top-ranked dragonflies as elite
            elite = population[:int(num_dragonflies / 2)]

            # Generate new dragonflies by crossover and mutation
            new_dragonflies = list()
            for i in range(int(num_dragonflies / 2)):
                parent1 = random.choice(elite)
                parent2 = random.choice(elite)
                child = list()
                for j in range(len(job)):
                    if random.random() < 0.5:
                        child.append(parent1.schedule[j])
                    else:
                        child.append(parent2.schedule[j])
                dragonfly = Dragonfly(child)
                new_dragonflies.append(dragonfly)

            # Evaluate fitness of new dragonflies
            for dragonfly in new_dragonflies:
                dragonfly.evaluate(job, machine)

            # Add new dragonflies to population
            population.extend(new_dragonflies)

        # Select final schedule
        population.sort(key=lambda x: x.fitness[1])
        return population[0]


if __name__ == "__main__":
    # Define jobs and machines
    jobs = [Job([(0, "task1"), (1, "task2")], 10),
            Job([(1, "task1"), (2, "task2")], 5),
            Job([(2, "task1"), (0, "task2")], 15)]

    machines = [Machine({"task1": 5, "task2": 10}),
                Machine({"task1": 10, "task2": 5}),
                Machine({"task1": 15, "task2": 10})]

    # jobs = [Job([(0, 3), (1, 2), (2, 2)], 10),
    #         Job([(0, 1), (2, 1), (1, 3)], 8),
    #         Job([(1, 3), (2, 1)], 10),
    #         Job([(0, 2), (1, 1)], 5)]
    # machines = [Machine([3, 2, 1, 3]),
    #             Machine([3, 1, 3, 2]),
    #             Machine([2, 3, 2, 1])]

    # Run BDA algorithm
    da = DragonFlyAlgorithm()
    bda = da.bda(jobs, machines, 10, 100)
    moda = da.moda(jobs, machines, 10, 100)

    # Print final schedule
    print(f'Basic Dragonfly Algorithm (BDA) fitness={bda.fitness[0]}, and schedule={bda.schedule}')
    print(f'Multi-objective Dragonfly Algorithm (MODA) fitness={moda.fitness[1]}, and schedule={moda.schedule}')
