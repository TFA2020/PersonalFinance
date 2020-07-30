def calc_saving(income, goal, time, balance=0, expenses=0):
    # time in terms of years
    time = float(time)
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

        if goal > 12 * income * time:
            saved_percent = round(income * time * 12/goal*100, 2)

            # format all the numbers to include 2 decimal places and commas if necessary
            max_saved = '{0:,.2f}'.format(round(income*time*12, 2))
            goal = '{0:,.2f}'.format(round(goal,2))
            return f'if you save all of your income, you will be able to save up to {saved_percent}% or ${max_saved} of ${}'
        else:
            # '{0:,.2f}'.format(value) = 2 decimal places and commas for every 4th digit "1,000"
            monthly_goal = '{0:,.2f}'.format(round(goal/time/12, 2))
            allowance = '{0:,.2f}'.format(round(income-monthly_goal,2))
            return f'for each of the {time * 12} months you will be saving for, you need to save ${monthly_goal} and you can spend ${allowance}'
