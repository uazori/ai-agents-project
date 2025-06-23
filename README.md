# AI Agents Project

## Overview
The AI Agents Project is a Python-based framework for creating intelligent agents that can act, learn, and reset their state based on interactions with their environment. This project provides a simple yet extensible structure for developing and testing AI agents.

## Features
- **Agent Class**: The core functionality is encapsulated in the `Agent` class, which includes methods for acting, learning from feedback, and resetting its state.
- **Testing**: Comprehensive unit tests are provided to ensure the reliability of the agent's methods.

## Installation
To install the project, clone the repository and install the required dependencies using pip:

```bash
git clone <repository-url>
cd ai-agents-project
pip install -r requirements.txt
```

## Usage
To use the `Agent` class, you can import it from the `src` package:

```python
from src.agent import Agent

# Create an instance of the Agent
agent = Agent()

# Use the agent's methods
action = agent.act(input_data)
agent.learn(feedback)
agent.reset()
```

## Running Tests
To run the tests for the project, use pytest:

```bash
pytest tests/
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.