import random as rd
from tkinter import *
import tkinter.ttk as ttk
from ttkbootstrap import Style


def fc_edd(processing_times, due_dates, penalties):
    # Sort jobs in ascending order of due dates
    jobs = list(zip(processing_times, due_dates, penalties))
    sorted_jobs = sorted(jobs, key=lambda x: x[1])
    sorted_indices = [i for i, _ in sorted(enumerate(due_dates), key=lambda pair: pair[1])]
  
    # Initialize completion times and total penalty
    completions = []
    total_penalty = 0

    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    # Loop through the sorted jobs and assign completion times
    for i, (job, due_date, penalty) in enumerate(sorted_jobs):
        index = sorted_indices[i]
        if len(completions) == 0:
            completions.append(job)
        else:
            completions.append(completions[-1] + job)

        # Update total penalty
        penalty_for_job = max(0, completions[-1] - due_date) * penalty
        total_penalty += penalty_for_job
        print("{:^5} {:^15} {:^10}".format(f'{sorted_indices[i] + 1:2}', f'{penalty_for_job:5}', f'{completions[-1]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')
    
    return 


def fc_spt(processing_times, due_dates, penalties):
    # Sort jobs in ascending order of processing times
    jobs = list(zip(processing_times, due_dates, penalties))
    sorted_jobs = sorted(jobs, key=lambda x: x[0])
    sorted_indices = [i for i, _ in sorted(enumerate(processing_times), key=lambda pair: pair[1])]

    # Initialize completion times and total penalty
    completions = []
    total_penalty = 0

    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    # Loop through the sorted jobs and assign completion times
    for i, (job, due_date, penalty) in enumerate(sorted_jobs):
        index = sorted_indices[i]
        if len(completions) == 0:
            completions.append(job)
        else:
            completions.append(completions[-1] + job)

        # Update total penalty
        penalty_for_job = max(0, completions[-1] - due_date) * penalty
        total_penalty += penalty_for_job
        print("{:^5} {:^15} {:^10}".format(f'{sorted_indices[i] + 1:2}', f'{penalty_for_job:5}', f'{completions[-1]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')
    
    return


def fc_lpul(processing_times, due_dates, penalties):
    # Compute U
    U = [penalty / processing_time for processing_time, penalty in zip(processing_times, penalties)]

    # Sort jobs in descending order of U
    jobs = list(zip(processing_times, due_dates, penalties, U))
    sorted_jobs = sorted(jobs, key=lambda x: x[3], reverse=True)
    sorted_indices = [i for i, _ in sorted(enumerate(U), key=lambda pair: pair[1], reverse=True)]

    # Initialize completion times and total penalty
    completions = []
    total_penalty = 0

    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    # Loop through the sorted jobs and assign completion times
    for i, (job, due_date, penalty, U) in enumerate(sorted_jobs):
        index = sorted_indices[i]
        if len(completions) == 0:
            completions.append(job)
        else:
            completions.append(completions[-1] + job)

        # Update total penalty
        penalty_for_job = max(0, completions[-1] - due_date) * penalty
        total_penalty += penalty_for_job
        print("{:^5} {:^15} {:^10}".format(f'{sorted_indices[i] + 1:2}', f'{penalty_for_job:5}', f'{completions[-1]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')
    
    return


def fc_spt_lpul(processing_times, due_dates, penalties):
    # Compute U
    U = [penalty / processing_time for processing_time, penalty in zip(processing_times, penalties)]

    # Sort jobs in ascending order of processing time
    # In case of tie, sort by descending order of U
    jobs = list(zip(processing_times, due_dates, penalties, U))
    sorted_jobs = sorted(jobs, key=lambda x: (x[0], -x[3]))
    sorted_indices = [i for i, _ in sorted(enumerate(jobs), key=lambda pair: (pair[1][0], -pair[1][3]))]

    # Initialize completion times and total penalty
    completions = []
    total_penalty = 0

    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    # Loop through the sorted jobs and assign completion times
    for i, (job, due_date, penalty, U) in enumerate(sorted_jobs):
        index = sorted_indices[i]
        if len(completions) == 0:
            completions.append(job)
        else:
            completions.append(completions[-1] + job)

        # Update total penalty
        penalty_for_job = max(0, completions[-1] - due_date) * penalty
        total_penalty += penalty_for_job
        print("{:^5} {:^15} {:^10}".format(f'{sorted_indices[i] + 1:2}', f'{penalty_for_job:5}', f'{completions[-1]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')
    
    return


def fc_swpt(processing_times, due_dates, penalties):
    # Compute S
    S = [processing_time / penalty for processing_time, penalty in zip(processing_times, penalties)]

    # Sort jobs in ascending order of S
    jobs = list(zip(processing_times, due_dates, penalties, S))
    sorted_jobs = sorted(jobs, key=lambda x: x[3])
    sorted_indices = [i for i, _ in sorted(enumerate(S), key=lambda pair: pair[1])]

    # Initialize completion times and total penalty
    completions = []
    total_penalty = 0

    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    # Loop through the sorted jobs and assign completion times
    for i, (job, due_date, penalty, S) in enumerate(sorted_jobs):
        index = sorted_indices[i]
        if len(completions) == 0:
            completions.append(job)
        else:
            completions.append(completions[-1] + job)

        # Update total penalty
        penalty_for_job = max(0, completions[-1] - due_date) * penalty
        total_penalty += penalty_for_job
        print("{:^5} {:^15} {:^10}".format(f'{sorted_indices[i] + 1:2}', f'{penalty_for_job:5}', f'{completions[-1]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')
    
    return


def fc_wt_lpul(processing_times, due_dates, penalties):
    # Compute U
    U = [penalty / processing_time for processing_time, penalty in zip(processing_times, penalties)]

    # Sort jobs in descending order of penalty
    # In case of tie, sort by descending order of U
    jobs = list(zip(processing_times, due_dates, penalties, U))
    sorted_jobs = sorted(jobs, key=lambda x: (-x[2], -x[3]))
    sorted_indices = [i for i, _ in sorted(enumerate(jobs), key=lambda pair: (-pair[1][2], -pair[1][3]))]

    # Initialize completion times and total penalty
    completions = []
    total_penalty = 0

    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    # Loop through the sorted jobs and assign completion times
    for i, (job, due_date, penalty, U) in enumerate(sorted_jobs):
        index = sorted_indices[i]
        if len(completions) == 0:
            completions.append(job)
        else:
            completions.append(completions[-1] + job)

        # Update total penalty
        penalty_for_job = max(0, completions[-1] - due_date) * penalty
        total_penalty += penalty_for_job
        print("{:^5} {:^15} {:^10}".format(f'{sorted_indices[i] + 1:2}', f'{penalty_for_job:5}', f'{completions[-1]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')
    
    return


def fc_cr(processing_times, due_dates, penalties):
    # Initialize variables to keep track of scheduled jobs, completion times, and total penalty
    n = len(processing_times)
    scheduled_jobs = []
    completions = []
    total_penalty = 0

    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    # Loop through the sorted jobs and assign completion times
    while len(scheduled_jobs) < n:
        T = sum([processing_times[i] for i in scheduled_jobs])
        cr = [((due_dates[i] - T) / processing_times[i])
              if i not in scheduled_jobs else float('inf') for i in range(n)]

        # Find the next job to schedule
        next_job = cr.index(min(cr))
        scheduled_jobs.append(next_job)
        completions.append(T + processing_times[next_job])

        # Update total penalty
        penalty = max(0, completions[-1] - due_dates[next_job]) * penalties[next_job]
        total_penalty += penalty
        print("{:^5} {:^15} {:^10}".format(f'{next_job + 1:2}', f'{penalty:5}', f'{completions[-1]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')
    
    return


def fc_ga(processing_times, due_dates, penalties):
    # Function to calculate the penalty for a given schedule
    num_jobs = len(penalties)
    population_size = 0
    generations = 100
    for i in range(1, num_jobs+1, 5):
        population_size += 30
        generations += 30*i
#     print(population_size)
#     print(generations)
#     print('-------')

    def calculate_penalty(schedule):
        completions = [processing_times[schedule[0]]]
        total_penalty = 0
        penalty_for_job = [0 for i in range(len(schedule))]

        for i in range(1, len(schedule)):
            completions.append(completions[i - 1] + processing_times[schedule[i]])
            penalty_for_job[schedule[i]] = max(0, completions[i] - due_dates[schedule[i]]) * penalties[schedule[i]]
            total_penalty += penalty_for_job[schedule[i]]

        return completions, total_penalty, penalty_for_job

    # Create initial population
    population = [[i for i in range(len(processing_times))] for _ in range(population_size)]
    rd.shuffle(population)

    # Loop through generations
    for _ in range(generations):
        # Select parents
        parents = rd.sample(population, population_size)

        # Crossover
        offspring = []
        for i in range(0, population_size, 2):
            parent1, parent2 = parents[i], parents[i + 1]
            crossover_point = rd.randint(1, len(parent1) - 1)
            offspring.append(parent1[:crossover_point] + [x for x in parent2 if x not in parent1[:crossover_point]])
            offspring.append(parent2[:crossover_point] + [x for x in parent1 if x not in parent2[:crossover_point]])

        # Mutation
        for i in range(population_size):
            if rd.random() < 0.1:
                mutation_point1 = rd.randint(0, len(offspring[i]) - 1)
                mutation_point2 = rd.randint(0, len(offspring[i]) - 1)
                offspring[i][mutation_point1], offspring[i][mutation_point2] = offspring[i][mutation_point2], \
                    offspring[i][mutation_point1]

        # Select survivors
        population = sorted(population + offspring, key=lambda x: calculate_penalty(x)[1])[:population_size]

    final_schedule = population[0]
    completions, total_penalty, penalty_for_job = calculate_penalty(final_schedule)
    
    print("{:^5} {:^15} {:^10}".format('Job', 'Penalty', 'Completion Time(Days)'))
    
    for i in range(len(final_schedule)):
        print("{:^5} {:^15} {:^10}".format(f'{final_schedule[i] + 1:2}', f'{penalty_for_job[final_schedule[i]]:5}', f'{completions[i]:11}'))
    print('-------------------------------------------')
    print(f" Makespan = {completions[-1]} Days")
    print(f" Total penalty = {total_penalty}")
    print('-------------------------------------------')

    return


root = Tk()
root.title("Single Machine Scheduling")
root.geometry("300x170")
# root.option_add('*font', 'tah-oma 9 bold')
frame = Frame(root)
frame.place(width=300, height=155, x=0, y=0)
style = Style(theme='flatly')
Label(frame, text="----  Method  ----").pack(pady=10)
choice = StringVar(value="")
combo = ttk.Combobox(textvariable=choice, style='secondary', state='readonly')
combo["values"] = ("EDD", "SPT", "LPUL", "SPT-LPUL", "SWPT", "WT-LPUL", "CR", "GA")
combo.pack(pady=40)

Label(frame, text="Number of job").place(x=50, y=85)
entry1 = ttk.Entry(frame, width=8, style='secondary')
entry1.place(x=175, y=80)


def job_data():
    selected_value = choice.get()
    print(" Selected Method:", selected_value)
    
    num_jobs = int(entry1.get())
    job = Toplevel(root)
    job.geometry("680x330")
    job.title("Enter job schedule")

    scrollbar = Scrollbar(job)
    scrollbar.pack(side=RIGHT, fill=Y)

    canvas = Canvas(job, yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.config(command=canvas.yview)

    frame_job = Frame(canvas)
    canvas.create_window((0, 0), window=frame_job, anchor='nw')

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    my_entries = []
    def cal():
        processing_time = []
        due_date = []
        penalty = []

        count = 0
        for i in range(len(my_entries)):
            if count == 0:
                processing_time.append(int(my_entries[i].get()))
            if count == 1:
                due_date.append(int(my_entries[i].get()))
            if count == 2:
                penalty.append(int(my_entries[i].get()))

            count += 1
            if count == 3:
                count = 0

        if selected_value == 'EDD':
            fc_edd(processing_time, due_date, penalty)
        if selected_value == 'SPT':
            fc_spt(processing_time, due_date, penalty)
        if selected_value == 'LPUL':
            fc_lpul(processing_time, due_date, penalty)
        if selected_value == 'SPT-LPUL':
            fc_spt_lpul(processing_time, due_date, penalty)
        if selected_value == 'SWPT':
            fc_swpt(processing_time, due_date, penalty)
        if selected_value == 'WT-LPUL':
            fc_wt_lpul(processing_time, due_date, penalty)
        if selected_value == 'CR':
            fc_cr(processing_time, due_date, penalty)
        if selected_value == 'GA':
            fc_ga(processing_time, due_date, penalty)

    for x in range(num_jobs):
        Label(frame_job, text="Job{}".format(x + 1)).grid(row=x + 1, column=0, padx=10, pady=10)

        if x == 0:
            Label(frame_job, text="Number of job").grid(row=0, column=0, padx=10, pady=10)
            Label(frame_job, text="Processing Time (min.)").grid(row=0, column=1, padx=10, pady=10)
            Label(frame_job, text="Due Date (days)").grid(row=0, column=2, padx=10, pady=10)
            Label(frame_job, text="Penalty").grid(row=0, column=3, padx=10, pady=10)

        for y in range(3):
            my_entry = Entry(frame_job)
            my_entry.grid(row=x + 1, column=y + 1, pady=5, padx=5)
            my_entries.append(my_entry)

    my_button = ttk.Button(frame_job, text='Sort Job', command=cal)
    my_button.grid(row=x + 2, column=3, pady=10)

    frame_job.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

button1 = ttk.Button(frame, text="Cancel", style='danger.TButton', width=6, command=root.destroy)
button1.place(x=155, y=120)
button2 = ttk.Button(frame, text="OK", style='success.TButton', width=6, command=job_data)
button2.place(x=75, y=120)

root.mainloop()