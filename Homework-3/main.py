import os
import csv


csv_path = os.path.join("Resources", "budget_data.csv")


with open(csv_path, newline="") as file:

    budget_data_reader = csv.reader(file, delimiter=",")

    csv_header = next(budget_data_reader)

    row_count = 0
    net_total = 0
    changes = []
    row_val = int(next(budget_data_reader)[1])
    row_val_2 = row_val
    months = []

    for row in budget_data_reader:
        row_count += 1
        net_total += int(row[1])


        change = int(row[1]) - row_val
        changes.append(change)
        row_val = int(row[1])

        months.append(row[0])

    greatest_increase = max(changes)
    increase_index = changes.index(greatest_increase)

    greatest_decrease = min(changes)
    decrease_index = changes.index(greatest_decrease)

    greatest_increase_month = months[increase_index]
    greatest_decrease_month = months[decrease_index]

    # To account for second next()
    row_count = row_count + 1
    net_total = net_total + row_val_2


    average_change = round(sum(changes) / len(changes),2)




print("Financial Analysis")
print("----------------------------")
print(f"Total Months: {row_count}")
print(f"Total: ${net_total}")
print(f"Average Change: ${average_change}")
print(f"Greatest Increase in Profits: {greatest_increase_month} (${greatest_increase})")
print(f"Greatest Decrease in Profits: {greatest_decrease_month} (${greatest_decrease})")


results = open("Financial_Analysis.txt", 'w')
results.write(f"""Financial Analysis
----------------------------
Total Months: {row_count}
Total: ${net_total}
Average Change: ${average_change}
Greatest Increase in Profits: {greatest_increase_month} (${greatest_increase})
Greatest Decrease in Profits: {greatest_decrease_month} (${greatest_decrease})
""")
