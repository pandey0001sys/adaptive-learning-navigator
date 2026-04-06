# #  Adaptive Learning Navigator

A Reinforcement Learning-based system where an AI agent learns efficient study strategies by maximizing knowledge gain and minimizing time.

##  Features

* Custom learning environment
* AI agent simulation
* Multiple learning actions (easy, medium, hard, revise, skip)
* Performance scoring system

##  Concept

The project is based on Reinforcement Learning:

* Agent → AI learner
* Environment → Learning system
* State → Knowledge level, time
* Action → Resource selection
* Reward → Learning gain vs time penalty

##  Evaluation

**Score = Learning Achieved ÷ Time Taken**

##  Tech Stack

* Python
* Gradio
* Reinforcement Learning (concept-based)

##  Project Structure

env.py
agent.py
app.py
requirements.txt
README.md

##  Run Locally

pip install -r requirements.txt
python app.py

##  Deployment

Deploy using Hugging Face Spaces (Gradio SDK).

