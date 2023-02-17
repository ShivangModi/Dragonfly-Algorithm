import random


class Job:
    def __init__(self, tasks, due_date):
        self.tasks = tasks
        self.due_date = due_date


class Machine:
    def __init__(self, processing_times):
        self.processing_times = processing_times


class Dragonfly:
    def __init__(self, schedule):
        self.schedule = schedule
        self.fitness = 0

    def mutate(self, machines):
        for i in range(len(self.schedule)):
            if random.random() < 0.1:
                self.schedule[i] = random.sample(range(len(machines)), len(self.schedule[i]))

    def evaluate(self, jobs, machines):
        makespan = 0
        tardiness = 0
        for job in jobs:
            completion_time = 0
            for task in job.tasks:
                machine = machines[task[0]]
                processing_time = machine.processing_times[task[1]]
                completion_time += processing_time
            makespan = max(makespan, completion_time)
            tardiness += max(0, completion_time - job.due_date)
        self.fitness = makespan + tardiness


def moda(jobs, machines, num_dragonflies, num_iterations, alpha, beta):
    # Initialize population of dragonflies randomly
    population = []
    for i in range(num_dragonflies):
        schedule = []
        for job in jobs:
            schedule.append(random.sample(range(len(machines)), len(job.tasks)))
        dragonfly = Dragonfly(schedule)
        dragonfly.evaluate(jobs, machines)
        population.append(dragonfly)

    # Run MODA algorithm
    for i in range(num_iterations):
        # Sort dragonflies in non-ascending order based on fitness
        population.sort(key=lambda x: x.fitness, reverse=True)

        # Select top-ranked dragonflies as elite
        elite = population[:int(num_dragonflies / 2)]

        # Generate new dragonflies by crossover and mutation
        new_dragonflies = []
        for i in range(int(num_dragonflies / 2)):
            parent1 = random.choice(elite)
            parent2 = random.choice(elite)
            child = []
            for j in range(len(jobs)):
                if random.random() < 0.5:
                    child.append(parent1.schedule[j])
                else:
                    child.append(parent2.schedule[j])
            dragonfly = Dragonfly(child)
            dragonfly.mutate(machines)
            new_dragonflies.append(dragonfly)

        # Evaluate fitness of new dragonflies
        for dragonfly in new_dragonflies:
            dragonfly.evaluate(jobs, machines)

        # Add new dragonflies to population
        population.extend(new_dragonflies)

    # Select final schedule
    population.sort(key=lambda x: x.fitness)
    return population[0]


# Define jobs and machines
jobs = [Job([(0, "task1"), (1, "task2")], 10),
        Job([(1, "task1"), (2, "task2")], 5),
        Job([(2, "task1"), (0, "task2")], 15)]
machines = [Machine({"task1": 5, "task2": 10}),
            Machine({"task1": 10, "task2": 5}),
            Machine({"task1": 15, "task2": 10})]

# Run MODA algorithm
best_dragonfly = moda(jobs, machines, 10, 100, 1, 1)

# Print final schedule
print(best_dragonfly.fitness, best_dragonfly.schedule)     # each list represent as job, and it displays in which machine task is working
