
def calc_saving(income, goal, time, balance=0, expenses=0):
    # time in terms of years
    time = int(time)
    balance = float(balance)
    # income in terms of month
    income = float(income)
    goal = float(goal)
    if income < expenses:
        return f"you are overspending by ${abs(round(income-expenses),2)}"
    else:
        # the "new" income is after expenses are deducted
        income = income - expenses
        # if current balance is less than goal, subtract it from goal, otherwise ignore balance
        if goal > balance:
            goal = goal - balance
        if goal > 12*income*time:
            saved_percent = round(income*time*12/goal*100, 2)
            max_saved = round(income*time*12, 2)
            return f'if you save all of your income, you will be able to save up to {saved_percent}% or ${max_saved} of ${round(goal,2)}'
        monthly_goal = round(goal/time/12, 2)
        return f'for each of the {year*12} months, you will have to save ${monthly_goal} and you can spend ${round(income-monthly_goal,2)}'
