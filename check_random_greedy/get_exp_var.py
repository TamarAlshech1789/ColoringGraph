import numpy as np
import statistics

def expected_value(values, weights):
    values = np.asarray(values)
    weights = np.asarray(weights)
    return (values * weights).sum() / weights.sum()


results = []
all_results = []
num = [0 for i in range(100)]
for i in range(1,101):
    file_name = "results_" + str(i) + '.txt'
    with open(file_name) as f:
        lines = f.readlines()

    result = float(lines[0])
    all_results.append((result))
    if not result in results:
        results.append(result)
    num[results.index(result)] += 1

prob = []
for i, r in enumerate(results):
    prob.append(float(num[i])/ 100)

print('the expectation is - ', expected_value(results, prob))

output = statistics.variance(all_results)

print('the variance is - ', output)