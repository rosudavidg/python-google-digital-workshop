# Init list
l = [7, 8, 9, 2, 3, 1, 4, 10, 5, 6]

# Print sorted list
print(sorted(l))

# Prin sorted list in descending order
print(sorted(l, reverse=True))

# Print only even index
print(l[::2])

# Print only odd index
print(l[1::2])

# Print 3-multipliers
print(list(filter(lambda e: e % 3 == 0, l)))
