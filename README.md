# Groq Terminal


**Groq Terminal** is a powerful, terminal-based interface for interacting with Large Language Models (LLMs) using the Groq API. Designed for developers and enthusiasts who prefer a command-line experience, Groq Terminal offers a rich set of features, including multi-tabbed conversations, model switching, conversation history management, and more—all enhanced with a visually appealing interface using [Rich](https://github.com/Textualize/rich).

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Commands](#available-commands)
- [Supported Models](#supported-models)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Interactive Command-Line Interface**: Engage with LLMs directly from your terminal.
- **Multi-Tabbed Conversations**: Manage multiple conversation threads simultaneously.
- **Model Management**: Switch between various models offered by Groq effortlessly.
- **Conversation History**: Save, load, and view conversation histories.
- **Rich Text Rendering**: Enhanced readability with Markdown support and colored outputs.
- **Command Autocompletion**: Speed up your workflow with intelligent command suggestions.
- **Customizable Prompts**: Tailor the terminal prompt to your preference.
- **Error Handling**: Comprehensive error visualization using Rich's traceback.

## Demo

![Groq Terminal Demo](https://github.com/Rohit-Yadav-47/Terminal_LLM/blob/main/demo.gif?raw=true)

*Note: Replace the above link with an actual GIF or screenshot showcasing the terminal in action.*

## Installation

### Prerequisites

- **Python 3.8+**: Ensure you have Python installed. You can download it from [here](https://www.python.org/downloads/).
- **Git**: To clone the repository. Download from [here](https://git-scm.com/downloads).

### Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Rohit-Yadav-47/Terminal_LLM.git
   cd Terminal_LLM
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Obtain Groq API Key**

   - Sign up or log in to your [Groq account](https://groq.com/).
   - Navigate to the API section to generate your API key.

2. **Set Up API Key**

   - Open `terminal.py` in a text editor.
   - Locate the following line:

     ```python
     self.api_key = "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"  # Replace with your GROQ API key
     ```

   - Replace the placeholder API key with your actual Groq API key:

     ```python
     self.api_key = "your_actual_groq_api_key_here"
     ```

   - **Security Tip**: For enhanced security, consider using environment variables or a configuration file to store your API key instead of hardcoding it.

## Usage

Launch the Groq Terminal by running the `terminal.py` script:

```bash
python terminal.py
```

Upon launching, you'll be greeted with a welcome message. You can start interacting with the LLM by typing your queries or commands.

### Example Interaction

```
Welcome to Groq Terminal!
Type /help for available commands

default> Hello, how are you?
Assistant:
I'm doing well, thank you! How can I assist you today?

default> /newtab ProjectIdeas
New tab 'ProjectIdeas' created.

default> /switch ProjectIdeas
Switched to tab 'ProjectIdeas'.

ProjectIdeas> Can you suggest some project ideas for a machine learning beginner?
Assistant:
Certainly! Here are a few project ideas:
1. **Spam Email Classifier**: Build a model to classify emails as spam or not spam.
2. **Image Classification**: Create a classifier that can identify different objects in images.
3. **Sentiment Analysis**: Analyze the sentiment of tweets or product reviews.
4. **Recommendation System**: Develop a system to recommend movies or products based on user preferences.
5. **Chatbot**: Create a simple chatbot that can answer basic questions.
```

## Available Commands

Groq Terminal supports a variety of commands to enhance your interaction experience. Commands are prefixed with a forward slash (`/`).

### General Commands

- `/help`  
  **Description**: Show the help message with all available commands.

- `/exit`  
  **Description**: Exit the Groq Terminal application.

- `/clear`  
  **Description**: Clear the conversation history of the current tab.

### Conversation Management

- `/save [filename]`  
  **Description**: Save the current conversation to a file. If no filename is provided, a timestamped default name is used.

  **Example**:  
  `/save my_conversation.json`

- `/load <filename>`  
  **Description**: Load a conversation from a file into the current tab.

  **Example**:  
  `/load my_conversation.json`

- `/history`  
  **Description**: Display the conversation history of the current tab.

### Model Management

- `/model`  
  **Description**: Switch between available models. Displays a table of supported models and prompts for selection.

### Tab Management

- `/tabs`  
  **Description**: Manage conversation tabs. Displays available tab management commands.

- `/newtab <tab_name>`  
  **Description**: Create a new conversation tab with the specified name.

  **Example**:  
  `/newtab Research`

- `/closetab <tab_name>`  
  **Description**: Close an existing conversation tab. The default tab cannot be closed.

  **Example**:  
  `/closetab Research`

- `/listtabs`  
  **Description**: List all active conversation tabs, highlighting the current one.

- `/switch <tab_name>`  
  **Description**: Switch to a different conversation tab.

  **Example**:  
  `/switch default`

## Supported Models

Groq Terminal supports multiple models provided by Groq. You can switch between them using the `/model` command. Below is a list of available models:

| Number | Model ID               | Developer | Context Window (Tokens) | Max Output Tokens | Max File Size |
|--------|------------------------|-----------|-------------------------|-------------------|---------------|
| 1      | gemma2-9b-it           | Google    | 8192                    | -                 | -             |
| 2      | llama-3.3-70b-versatile| Meta      | 128000                  | 32768             | -             |
| 3      | llama-3.1-8b-instant   | Meta      | 128000                  | 8192              | -             |
| 4      | llama-guard-3-8b       | Meta      | 8192                    | -                 | -             |
| 5      | llama3-70b-8192        | Meta      | 8192                    | -                 | -             |
| 6      | llama3-8b-8192         | Meta      | 8192                    | -                 | -             |
| 7      | mixtral-8x7b-32768     | Mistral   | 32768                   | -                 | -             |

**Note**: The availability and specifications of models are subject to change based on Groq's offerings. Always refer to the latest documentation or use the `/model` command to view current options.

## Contribution

Contributions are welcome! Whether it's reporting bugs, suggesting features, or improving documentation, your input is valuable.

### Steps to Contribute

1. **Fork the Repository**

   Click the "Fork" button at the top-right corner of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/your_username/Terminal_LLM.git
   cd Terminal_LLM
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

   Implement your feature or fix the bug.

5. **Commit Your Changes**

   ```bash
   git commit -m "Add feature: YourFeatureName"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Create a Pull Request**

   Go to the original repository and click on "New Pull Request". Provide a clear description of your changes.

### Code of Conduct

Please adhere to the [Code of Conduct](https://github.com/Rohit-Yadav-47/Terminal_LLM/blob/main/CODE_OF_CONDUCT.md) when interacting with this project.

## License

This project is licensed under the [MIT License](https://github.com/Rohit-Yadav-47/Terminal_LLM/blob/main/LICENSE).
