from random import randint, shuffle

finalOutput = []
# generate 980,000 rows with sum < 10,000
for _ in range(980000):
    finalOutput.append([randint(10, 2000) for _ in range(5)])

# generate 20,000 rows with sum > 10,000
for _ in range(20000):
    finalOutput.append([randint(20000,50000000) for _ in range(5)])

shuffle(finalOutput)

for row in finalOutput:
    print(f'{row[0]} {row[1]} {row[2]} {row[3]} {row[4]}')
