
def calc_saving(income, goal, time, balance=0, expenses=0):
    # time in terms of years
    time = int(time)
    balance = float(balance)
    # income in terms of month
    income = float(income)
    goal = float(goal)
    if income < expenses:
        return f"you are overspending by {abs(income-expenses)}"
    else:
        # the "new" income is after expenses are deducted
        income = income - expenses
        # if current balance is less than goal, subtract it from goal, otherwise ignore balance
        if goal > balance:
            goal = goal - balance
        if goal > 12*income*time:
            return f'you will be able to save up to {round(income*time*12/goal*100, 2)}%'
        monthly_goal = goal/time/12
        return f'you will have to save {round(monthly_goal,2)} and you can spend {round(income-monthly_goal,2)} every month'
