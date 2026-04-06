import gradio as gr
import matplotlib.pyplot as plt
from env import LearningEnv
from agent import Agent

env = LearningEnv()
agent = Agent()

history = []
steps = 0

# 🔁 AUTO RUN
def run_auto(difficulty):
    global history, steps
    state = env.reset()
    history = []
    steps = 0

    log = ""

    while True:
        steps += 1

        # difficulty based bias
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

            return log, f"🏁 Score: {round(score,2)}", plot_graph(), f"📊 Efficiency: {efficiency}%"

# 🎮 MANUAL CONTROL
def manual_step(action):
    global history, steps
    steps += 1

    state, reward, done = env.step(action)
    history.append((state[0], state[1]))

    text = f"Step {steps} → {action} | K={state[0]} | T={state[1]} | R={reward}"

    if done:
        score = state[0] / (state[1] + 1)
        text += f"\n🏁 Score: {round(score,2)}"

    return text, plot_graph()

# 📊 GRAPH
def plot_graph():
    if not history:
        return None

    k = [h[0] for h in history]
    t = [h[1] for h in history]

    plt.figure()
    plt.plot(t, k)
    plt.xlabel("Time")
    plt.ylabel("Knowledge")
    plt.title("Learning Curve")
    return plt

# 🔄 RESET
def reset():
    global history, steps
    history = []
    steps = 0
    env.reset()
    return "Reset Done", "", None, ""

# 🎨 UI DESIGN
with gr.Blocks(theme=gr.themes.Glass()) as demo:

    gr.Markdown("""
    # 🧠 Adaptive Learning Navigator  
    ### 🚀 AI Optimizes Learning using Reinforcement Learning
    """)

    with gr.Row():
        difficulty = gr.Dropdown(["Normal", "Easy", "Hard"], label="🎯 Select Mode")

    with gr.Row():
        log_box = gr.Textbox(label="📜 Simulation Log", lines=12)
        graph = gr.Plot(label="📊 Learning Graph")

    with gr.Row():
        score_box = gr.Textbox(label="🏁 Score")
        efficiency_box = gr.Textbox(label="⚡ Efficiency")

    auto_btn = gr.Button("⚡ Run Auto Simulation")

    gr.Markdown("## 🎮 Manual Control")

    manual_out = gr.Textbox(label="Manual Output")

    with gr.Row():
        gr.Button("Easy").click(lambda: manual_step("easy"), outputs=[manual_out, graph])
        gr.Button("Medium").click(lambda: manual_step("medium"), outputs=[manual_out, graph])
        gr.Button("Hard").click(lambda: manual_step("hard"), outputs=[manual_out, graph])
        gr.Button("Revise").click(lambda: manual_step("revise"), outputs=[manual_out, graph])
        gr.Button("Skip").click(lambda: manual_step("skip"), outputs=[manual_out, graph])

    reset_btn = gr.Button("🔄 Reset")

    auto_btn.click(run_auto, inputs=difficulty, outputs=[log_box, score_box, graph, efficiency_box])
    reset_btn.click(reset, outputs=[manual_out, log_box, graph, score_box])

demo.launch()