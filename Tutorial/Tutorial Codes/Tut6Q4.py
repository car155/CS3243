possible_actions = {"right":{"right", "down", "up"},
                    "up":{"up", "left", "right"}}

m = [[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]

def get_prob(seq, p, path_taken):
    if (len(seq) == 0):
        add_prob(path_taken, p)
    else:
        seq = seq.copy()
        a = seq.pop(0)
        for b in possible_actions[a]:
            if b == a:
                get_prob(seq, p*0.8, path_taken + [b])
            else:
                get_prob(seq, p*0.1, path_taken + [b])

def add_prob(path, prob):
    x = 2
    y = 0
    for a in path:
        x_next = x
        y_next = y
        if (a == "down"):
            x_next = min(2, x+1)
        elif (a == "up"):
            x_next = max(0, x-1)
        elif (a == "left"):
            y_next = max(0, y-1)
        else:
            y_next = min(3, y+1)

        if (x_next != 1 or y_next != 1):
            x = x_next
            y = y_next

    m[x][y] = m[x][y] + prob
    print(path, x, y, round(prob, 7))

get_prob(["up", "up", "right", "right", "right"], 1, [])
print(m)