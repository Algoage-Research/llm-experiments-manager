# Experiment manager for llm service

## Explanation

This tool is designed to make it convenient to iterate experiments, analysis and improvement for the LLM service, making it a valuable asset for any researcher or developer in the field.

### Key features include

**Automated Experiment Management**: The `src/main.py` script manages the interaction between a SystemAgent and a UserAgent, running experiments with different configurations and automatically storing the results for each experiment run in a MongoDB collection, thanks to the [sacred](https://github.com/IDSIA/sacred) library.

**Configuration Customization**: The `src/config.py` file allows users to specify the configuration for both the system and user agents. This includes the definition of success of chat services, the OpenAI model to be used, and the evaluation configuration.

**Evaluation Metrics**: The `src/evaluator.py` file provides a method to evaluate the user experience based on satisfaction and goal accomplishment metrics. These metrics are weighted to calculate a final score, which determines the success of the experiment.

**Result Viewer**: A built-in viewer, created with [streamlit](https://github.com/streamlit/streamlit), enables users to conveniently check the results and configurations of the experiments.

**Docker Support**: You need only docker to run this repository.

## Your Contribution is Welcome!

You can send PR, create issues or contact https://twitter.com/yasu_919 (it is Japanese user but you can send English DM)

## Setup

create `.credential.env` and write `OPENAI_API_KEY={your openai api key}`

## How to run

`docker compose up mongo`

`docker compose run main python main.py`

## How to view the results

`docker compose up viewer`

open http://localhost:8501
