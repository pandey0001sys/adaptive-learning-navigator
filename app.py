from fastapi import FastAPI
import gradio as gr
import matplotlib.pyplot as plt
from env import LearningEnv
from agent import Agent

# ----------- FASTAPI (OpenEnv API) -----------
app = FastAPI()

env = LearningEnv()
agent = Agent()

state_data = {"state": [0, 0, 100]}

@app.post("/reset")
def reset_api():
    state = env.reset()
    state_data["state"] = state
    return {"state": state}

@app.post("/step")
def step_api(action: dict):
    act = action.get("action", "easy")
    state, reward, done = env.step(act)
    state_data["state"] = state
    return {"state": state, "reward": reward, "done": done}

@app.get("/state")
def get_state():
    return state_data


# ----------- GRADIO UI (Tumhara same UI) -----------
history = []
steps = 0

def run_auto(difficulty):
    global history, steps
    state = env.reset()
    history = []
    steps = 0

    log = ""

    while True:
        steps += 1

        if difficulty == "Easy":
            action = "easy"
        elif difficulty == "Hard":
            action = "hard"
        else:
            action = agent.choose_action(state)

        state, reward, done = env.step(action)
        history.append((state[0], state[1]))

        log += f"Step {steps} → {action} | K={state[0]} | T={state[1]} | R={reward}\n"

        if done:
            score = state[0] / (state[1] + 1)
            efficiency = round((state[0] * 100) / (state[1] + 1), 2)

            return log, f"Score: {round(score,2)}", plot_graph(), f"Efficiency: {efficiency}%"


def manual_step(action):
    global history, steps
    steps += 1

    state, reward, done = env.step(action)
    history.append((state[0], state[1]))

    text = f"Step {steps} → {action} | K={state[0]} | T={state[1]} | R={reward}"

    if done:
        score = state[0] / (state[1] + 1)
        text += f"\nScore: {round(score,2)}"

    return text, plot_graph()


def plot_graph():
    if not history:
        return None

    k = [h[0] for h in history]
    t = [h[1] for h in history]

    plt.figure()
    plt.plot(t, k)
    return plt


def reset_ui():
    global history, steps
    history = []
    steps = 0
    env.reset()
    return "Reset Done", "", None, ""


with gr.Blocks() as demo:
    gr.Markdown("# Adaptive Learning Navigator")

    difficulty = gr.Dropdown(["Normal", "Easy", "Hard"])

    log_box = gr.Textbox(lines=10)
    graph = gr.Plot()

    score_box = gr.Textbox()
    efficiency_box = gr.Textbox()

    auto_btn = gr.Button("Run Auto")

    manual_out = gr.Textbox()

    gr.Button("Easy").click(lambda: manual_step("easy"), outputs=[manual_out, graph])
    gr.Button("Medium").click(lambda: manual_step("medium"), outputs=[manual_out, graph])
    gr.Button("Hard").click(lambda: manual_step("hard"), outputs=[manual_out, graph])

    reset_btn = gr.Button("Reset")

    auto_btn.click(run_auto, inputs=difficulty, outputs=[log_box, score_box, graph, efficiency_box])
    reset_btn.click(reset_ui, outputs=[manual_out, log_box, graph, score_box])


app = gr.mount_gradio_app(app, demo, path="/")
