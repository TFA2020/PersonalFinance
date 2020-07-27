
def calc_saving(income, goal, age, balance=0):
    years= 62- int(age)
    goal = float(goal)-balance
    income = float(income)
    if goal - 12*income*years > 0:
        return f'you will be able to save up to {round(income*years*12/goal*100, 2)}%'
    monthly_goal = goal/years/12
    return f'you will have to save {round(monthly_goal,2)} and you can spend {round(income-monthly_goal,2)} every month'
