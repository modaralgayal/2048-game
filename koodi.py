def count(t):
    positions = {}
    result = 0
    setValues = set(t)

    for index in range(len(t)):
        if t[index] not in positions:
            positions[t[index]] = []
    
        positions[t[index]].append(index)
    
    for value in setValues:
        for i, stock in enumerate(t):
            if stock == value * 2:
                for val in positions[value]:
                    if i > val:
                        result += 1
        t.pop(0)
    
    return result

if __name__ == "__main__":
    print(count([1, 2, 3, 4]))      # 2
    print(count([1, 1, 1, 1]))      # 0
    print(count([1, 2, 1, 2, 1, 2]))# 6
    print(count([5, 1, 3, 4, 1, 6]))# 1
