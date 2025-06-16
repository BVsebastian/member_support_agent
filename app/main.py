import gradio as gr
from agent.retriever import Retriever
from app.prompt_manager import get_system_prompt
from openai import OpenAI
import os
from dotenv import load_dotenv

#Load environment variables
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def respond(message):
    print(f"\nUser Question: {message}")  # Print the question
    
    # 1. Get system prompt with Alexa's identity
    system_prompt = get_system_prompt()
    
    # 2. Retrieve relevant FAQ chunks
    retriever = Retriever()
    relevant_chunks = retriever.retrieve_top_chunks(message)
    
    # 3. Build context with system prompt and FAQ chunks
    context = f"{system_prompt}\n\nRelevant Information:\n"
    for chunk in relevant_chunks:
        context += f"- {chunk['text']}\n"
    
    # 4. Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": message}
        ]
    )
    
    answer = response.choices[0].message.content
    print(f"\nAssistant Response: {answer}")  # Print the response
    return answer

# Create the Gradio interface
iface = gr.Interface(
    fn=respond,
    inputs=gr.Textbox(label="Ask a question"),
    outputs=gr.Textbox(label="Response"),
    title="Member Support AI Agent",
    description="Ask me anything about Horizon Bay Credit Union services!",
    examples=[
        "What documents do I need to open an account?",
        "How do I reset my password?",
        "What are the fees for a checking account?",
    ],
    flagging_mode="never"
)

if __name__ == "__main__":
    iface.launch()