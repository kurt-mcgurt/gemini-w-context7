import gradio as gr
from google import genai
# from google.genai import types # Not strictly needed for this basic app
import os

client = None
model_name = 'gemini-2.5-flash-preview-05-20'
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise KeyError("GEMINI_API_KEY not found in environment variables.")
    client = genai.Client(api_key=api_key)
    # Test client connection by listing models (optional, but good for early failure)
    # client.models.list() 
except KeyError:
    print("Error: The GEMINI_API_KEY environment variable is not set.")
    print("Please set it before running the script (e.g., export GEMINI_API_KEY='your_api_key')")
    exit()
except Exception as e:
    print(f"Error initializing the Gemini client: {e}")
    exit()

# The model object isn't explicitly created anymore with client.models.get_model
# The model name string is used directly in generate_content.

def chat_with_gemini(message, history):
    if not client:
        return "Error: Gemini client not initialized. Please check API key and restart."

    # MCP Tool Usage Note:
    # This Gradio app provides direct chat with Gemini.
    # To use MCP server tools (like @upstash/context7-mcp for documentation retrieval),
    # you would typically:
    # 1. Copy relevant code or questions from this chat.
    # 2. Paste it into your MCP-enabled coding assistant (e.g., Cursor, VS Code with MCP extension).
    # 3. Instruct the assistant to use the MCP tool (e.g., "Explain this code using context7").
    # This app does not directly invoke MCP tools. The following is a conceptual placeholder.

    if "use_mcp_tool_example" in message: # Example trigger phrase
        # This is a conceptual placeholder.
        # Actual MCP tool invocation would happen in your coding assistant.
        mcp_concept_output = "[MCP Tool Concept: User might ask context7 to find docs related to the current discussion]"
        # In a real integrated scenario, this might involve API calls to an MCP client proxy.
        # For now, we just append this note to the chat.
        # return f"Gemini's response to '{message}'... \n\n{mcp_concept_output}"
        # For this version, we'll let Gemini respond to the original message,
        # and the user can manually use MCP tools with the chat content.
        pass # Let Gemini handle the full message

    try:
        response = client.models.generate_content(model=model_name, contents=message)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini: {e}"

# Create the Gradio interface
iface = gr.ChatInterface(
    fn=chat_with_gemini,
    title="Gemini Chat with MCP Tools",
    description="Chat with Google Gemini. MCP tool integration is currently a placeholder.",
    examples=[["Hello, Gemini!"], ["What's the weather like today? (MCP placeholder)"]],
    theme="soft"
)

if __name__ == "__main__":
    # Make sure to forward port 7860 in your dev container or environment
    iface.launch(server_name="0.0.0.0", server_port=7860, share=True)
# in progress
