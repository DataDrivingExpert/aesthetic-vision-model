import os
import matplotlib.pyplot as plt

counter = {}

for i in range(24):
    counter[i] = 0

print(f"Counter initialized {counter=}")

train_path = "datasets/HLM/labels/train"
files = os.listdir(train_path)

for file in files:
    lines = [l for l in open(os.path.join(train_path, file), 'r').readlines()]
    for line in lines:
        counter[int(line.split()[0])] += 1

with open('output.txt', 'w') as f:
    for i in range(24):
        f.write(f"{i}: {counter[i]}\n")

fig, ax = plt.subplots()

ax.bar(list(counter.keys()), list(counter.values()))

ax.set_ylabel('Number of instances')
ax.set_title('Distribution of classes in the training set')

plt.savefig('class_distribution.png')
plt.show()