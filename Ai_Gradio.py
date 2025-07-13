# Step 1: Basic Gradio App
# A simple function and Gradio interface
import gradio as gr

def shout(text):
    print(f"Shout has been called with input: {text}")
    return text.upper()

# Basic app
basic_interface = gr.Interface(
    fn=shout,
    inputs="textbox",
    outputs="textbox",
    title="Basic Shout App",
    description="Enter text and see it in uppercase."
)
basic_interface.launch()

# Step 2: Sharing and Auto-launching in Browser
# Adding share=True and inbrowser=True for public sharing and browser auto-launch
shared_interface = gr.Interface(
    fn=shout,
    inputs="textbox",
    outputs="textbox",
    flagging_mode="never"
)
shared_interface.launch(share=True, inbrowser=True)

# Step 3: Force Dark Mode using Custom JavaScript
force_dark_mode_js = """
function refresh() {
    const url = new URL(window.location);
    if (url.searchParams.get('__theme') !== 'dark') {
        url.searchParams.set('__theme', 'dark');
        window.location.href = url.href;
    }
}
"""
dark_mode_interface = gr.Interface(
    fn=shout,
    inputs="textbox",
    outputs="textbox",
    flagging_mode="never",
    js=force_dark_mode_js
)
dark_mode_interface.launch()

# Step 4: Advanced Interface with Labels and Multiline Boxes
labeled_interface = gr.Interface(
    fn=shout,
    inputs=[gr.Textbox(label="Your message:", lines=6)],
    outputs=[gr.Textbox(label="Response:", lines=8)],
    flagging_mode="never"
)
labeled_interface.launch()

# Step 5: Integrate LLM (LLaMA 3.2 via Ollama)
import ollama

system_message = "You are a helpful assistant."

def message_llama(prompt):
    prompts = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    response = ollama.chat(
        model="llama3.2",
        messages=prompts
    )
    return response['message']['content'].strip()

llama_interface = gr.Interface(
    fn=message_llama,
    inputs=[gr.Textbox(label="Your message:", lines=6)],
    outputs=[gr.Textbox(label="Response:", lines=8)],
    flagging_mode="never"
)
llama_interface.launch()

# Step 6: LLaMA with Markdown Output
system_message = "You are a helpful assistant that responds in markdown."

markdown_interface = gr.Interface(
    fn=message_llama,
    inputs=[gr.Textbox(label="Your message:")],
    outputs=[gr.Markdown(label="Response:")],
    flagging_mode="never"
)
markdown_interface.launch()

# Step 7: Streaming LLM Output

def stream_llama(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    stream = ollama.chat(
        model='llama3.2',
        messages=messages,
        stream=True
    )

    result = ""
    for chunk in stream:
        content = chunk['message']['content']
        result += content
        yield result

streaming_interface = gr.Interface(
    fn=stream_llama,
    inputs=[gr.Textbox(label="Your message:")],
    outputs=gr.Textbox(label="Response", lines=20),
    flagging_mode="never"
)
streaming_interface.launch()
