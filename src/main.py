import openpyxl
import numpy as np

class TrainingProgram:
    squat_5RM = 0
    ohp_5RM = 0
    dl_5RM = 0
    bench_5RM = 0
    squat_program = {}

    bench_starting_weight = 0
    squat_starting_weight = 0
    ohp_starting_weight = 0
    dl_starting_weight = 0
    min_plate_weight = 1.25
    pr_week = 4
    set_interval = 0.1

    def __init__(self, training_days_per_week):
        self.training_days_per_week = training_days_per_week

        self.min_plate_weight = input_float("Enter minimum plate weight: ")
        self.pr_week = input_int("Enter week to match pr: ")
        self.squat_starting_weight = input_float("Enter heaviest squat lifted: ")
        squat_reps = input_int("Enter reps performed: ")

        
        self.squat_5RM = self.get_5RM(self.squat_starting_weight, squat_reps)
        self.squat_program = self.create_squat_program(self.squat_5RM)

    def get_5RM(self, test_weight, number_of_reps):
        calculated_1RM = test_weight/(1.0278-(0.0278*number_of_reps))

        return calculated_1RM*(1.0278-(0.0278*5))

    def get_starting_weight(self, calculated_5RM, pr_week,):
        return round(calculated_5RM*((1/1.025)**(pr_week - 1))
                /(2*self.min_plate_weight), 0)*2*self.min_plate_weight

    def create_squat_program(self, calculated_5RM):
        program = {{}}

        program["D1"]["W1"] = self.get_5_reps_scheme(calculated_5RM)

        for week in range(2, 12):
            weekly_5RM = program["D1"]["W{}".format(week - 1)]
            program["D1"]["W{}".format(week)] = self.get_5_reps_scheme(weekly_5RM)

            program["D2"]["W{}".format(week)] = program["D1"]["W{}".format(week)]
            program["D2"]["W{}".format(week)].append(program["D2"]["W{}".format(week)][2])

            program["D3"]["W{}".format(week)] = program["D2"]["W{}".format(week)][:3]
            program["D3"]["W{}".format(week)].append(program["D3"]["W{}".format(week)][-1])
        

    def get_5_reps_scheme(calculated_5RM):
        scheme = list(np.zeros(5))
        scheme[4] = calculated_5RM

        for i in range(1, 4):
            scheme[4-i] = round(calculated_5RM*(1 - self.set_interval*i)
                                /(2*self.min_plate_weight), 
                                0)*2*self.min_plate_weight

        return scheme



def input_int(text):
    try:
        number = int(input(text))
    except ValueError:
        print("Input an integer.")

    return number


def input_float(text):
    try:
        number = float(input(text))
    except ValueError:
        print("Input a float.")

    return number

def main():
    program = TrainingProgram(3)
    return 0


if __name__ == "__main__":
    main()
