import tkinter as tk
import random
grid = [
    ["S","F","F","F"],
    ["F","H","F","H"],
    ["F","F","F","H"],
    ["H","F","F","G"]
]
nrows, ncols = 4, 4
actions = [0,1,2,3]  # Left, Down, Right, Up
arrows = {0:"←", 1:"↓", 2:"→", 3:"↑"}
gamma, slip = 0.99, 0.1

def in_bounds(r,c): return 0<=r<nrows and 0<=c<ncols
def is_terminal(s): return grid[s[0]][s[1]] in ("H","G")

def move(s,a):
    r,c = s
    if a == 0: c -= 1
    elif a == 1: r += 1
    elif a == 2: c += 1
    elif a == 3: r -= 1
    return (r,c) if in_bounds(r,c) else s

# --- Value Iteration ---
def value_iteration():
    V = {(r,c): 0 for r in range(nrows) for c in range(ncols)}
    for _ in range(100):
        newV = V.copy()
        for s in V:
            if is_terminal(s): continue
            best = float('-inf')
            for a in actions:
                val = 0
                for b in actions:
                    prob = 0.9 if a == b else 0.1/3
                    ns = move(s,b)
                    r = 1 if grid[ns[0]][ns[1]] == "G" else 0
                    val += prob * (r + gamma * V[ns])
                best = max(best, val)
            newV[s] = best
        if max(abs(V[s]-newV[s]) for s in V) < 1e-4:
            break
        V = newV
    # derive policy
    policy = {}
    for s in V:
        if is_terminal(s):
            policy[s] = None
            continue
        policy[s] = max(actions, key=lambda a: sum(
            (0.9 if a == b else 0.1/3) * (
                (1 if grid[move(s,b)[0]][move(s,b)[1]] == "G" else 0)
                + gamma * V[move(s,b)]
            ) for b in actions))
    return policy

policy = value_iteration()
start = (0,0)
agent = start

# --- GUI with Tkinter ---
CELL = 80
root = tk.Tk()
root.title("Frozen Lake MDP - Simple GUI")

canvas = tk.Canvas(root, width=4*CELL, height=4*CELL, bg="white")
canvas.pack(pady=10)
msg = tk.Label(root, text="Press Step or Auto Run", font=("Arial",12))
msg.pack()

def draw():
    canvas.delete("all")
    for r in range(4):
        for c in range(4):
            color = {"S":"skyblue","F":"white","H":"salmon","G":"lightgreen"}[grid[r][c]]
            x, y = c*CELL, r*CELL
            canvas.create_rectangle(x, y, x+CELL, y+CELL, fill=color, outline="black")
            a = policy[(r,c)]
            if a != None and not is_terminal((r,c)):
                canvas.create_text(x+CELL/2, y+CELL/2, text=arrows[a], font=("Arial",14,"bold"))
            if (r,c) == agent:
                canvas.create_oval(x+20, y+20, x+CELL-20, y+CELL-20, fill="blue")
draw()

def step():
    global agent
    if is_terminal(agent): return
    a = policy[agent]
    if random.random() < slip:
        a = random.choice([x for x in actions if x != a])
    agent = move(agent, a)
    draw()
    if grid[agent[0]][agent[1]] == "G":
        msg.config(text="🎯 Goal Reached!")
    elif grid[agent[0]][agent[1]] == "H":
        msg.config(text="💀 Fell into Hole!")

def auto():
    def run():
        if is_terminal(agent): return
        step()
        root.after(500, run)
    run()

def reset():
    global agent
    agent = start
    draw()
    msg.config(text="Reset complete!")

frame = tk.Frame(root)
frame.pack()
tk.Button(frame, text="Step", width=10, command=step).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Auto Run", width=10, command=auto).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Reset", width=10, command=reset).grid(row=0, column=2, padx=5)

root.mainloop()
