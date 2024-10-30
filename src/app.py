import gradio as gr
from main import PolySummaryYT
from utils_app import button_timer, update_button

TRANSLATOR = PolySummaryYT()
LANGUAGES_LIST = TRANSLATOR.get_languages()

def translate_click_start(youtube_url, language, groq_key, openai_key):
    result_translation = TRANSLATOR.summarize_video(youtube_url, language, groq_key, openai_key)
    return result_translation["audio_path"], result_translation["text"]

def toggle_api_config(is_visible):
    return gr.update(visible=not is_visible), not is_visible

def embed_youtube_video(url):
    if "?v=" in url:
        video_id = url.split("?v=")[-1].split("&")[0]
    elif "shorts" in url:
        video_id = url.split("/")[-1].split(".")[0]
           
    embed_html = f'<iframe width="100%" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'
    return embed_html

custom_css = """
#app-container {
    background-color: #1a1a2e;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    max-width: 1200px;
    margin: 2rem auto;
    padding: 2rem;
}
#header {
    background: linear-gradient(90deg, #4a00e0, #8e2de2);
    border-radius: 15px;
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}
#header h1 {
    color: white;
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
#header p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.2rem;
}
.input-section, .output-section {
    background-color: #16213e;
    border-radius: 15px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.input-section h3, .output-section h3 {
    color: #4a00e0;
    margin-bottom: 1rem;
}
#translate-btn {
    background: linear-gradient(90deg, #4a00e0, #8e2de2);
    border: none;
    border-radius: 30px;
    color: white;
    font-size: 1.2rem;
    padding: 0.8rem 2rem;
    transition: all 0.3s ease;
}
#translate-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(78, 0, 224, 0.4);
}
#audio-output {
    background-color: #0f3460;
    border-radius: 10px;
    padding: 1rem;
}
#result-text {
    background-color: #0f3460;
    border-radius: 10px;
    color: white;
    font-family: 'Courier New', monospace;
    padding: 1rem;
}
#api-config-toggle {
    background-color: #4a00e0;
    border: none;
    border-radius: 15px;
    color: white;
    cursor: pointer;
    font-size: 1rem;
    padding: 0.5rem 1rem;
    margin-bottom: 1rem;
    transition: background-color 0.3s ease;
}
#api-config-toggle:hover {
    background-color: #5a10f0;
}
"""

with gr.Blocks(css=custom_css) as iface:
    with gr.Column(elem_id="app-container"):
        gr.HTML(
            """
            <div id="header">
                <h1>🌐 PolySummaryYT</h1>
                <p>Transform YouTube videos into multilingual summaries with ease</p>
            </div>
            """
        )

        with gr.Row():
            with gr.Column(elem_classes="input-section"):
                api_config_visible = gr.State(False)
                api_config_toggle = gr.Button("Show API Configuration", elem_id="api-config-toggle")
                
                with gr.Column(visible=False) as api_config_content:
                    gr.Markdown("### 🔑 API Configuration")
                    groq_key_input = gr.Textbox(
                        label="GROQ API Key",
                        placeholder="Enter your GROQ API key",
                        type="password",
                        info="Used for transcription and translation"
                    )
                    openai_key_input = gr.Textbox(
                        label="OpenAI API Key used for Text-to-Speech ",
                        placeholder="Enter your OPENAI API KEY here! (Used for Text-to-Speech)",
                        type="password",
                        info="- leave it empty for free text to speech model usage"
                    )

                gr.Markdown("### 🎥 Video Input")
                youtube_url = gr.Textbox(
                    label="YouTube URL",
                    placeholder="https://www.youtube.com/watch?v=...",
                    info="Paste the full YouTube video URL here"
                )
                
                language = gr.Dropdown(
                    choices=LANGUAGES_LIST,
                    label="Target Language",
                    value=LANGUAGES_LIST[0],
                    interactive=True,
                    info="Select the language for the summary"
                )
                translate_btn = gr.Button("Summarize and Translate", elem_id="translate-btn")

        with gr.Row(elem_classes="output-section"):
            with gr.Column():
                gr.Markdown("### 🔊 Audio Summary")
                audio_output = gr.Audio(label="Translated Audio", elem_id="audio-output")
                video_embed = gr.HTML(elem_id="video-embed")
            
            with gr.Column():
                gr.Markdown("### 📝 Text Summary")
                result_text = gr.Textbox(
                    label="Translation Result",
                    interactive=False,
                    elem_id="result-text",
                    lines=10
                )

        youtube_url.change(
            fn=embed_youtube_video,
            inputs=[youtube_url],
            outputs=[video_embed]
        )

        api_config_toggle.click(
            toggle_api_config,
            inputs=[api_config_visible],
            outputs=[api_config_content, api_config_visible]
        ).then(
            lambda x: "Hide API Configuration" if x else "Show API Configuration",
            inputs=[api_config_visible],
            outputs=[api_config_toggle]
        )

        language.change(
            update_button,
            inputs=language,
            outputs=translate_btn
        )

        translate_btn.click(
            fn=lambda: gr.update(interactive=False, value="Processing..."),
            inputs=None,
            outputs=translate_btn
        ).then(
            fn=translate_click_start,
            inputs=[youtube_url, language, groq_key_input, openai_key_input],
            outputs=[audio_output, result_text]
        ).then(
            fn=button_timer,
            inputs=None,
            outputs=None
        ).then(
            fn=lambda: gr.update(interactive=True, value="Summarize and Translate"),
            inputs=None,
            outputs=translate_btn
        )

if __name__ == "__main__":
    iface.launch(share=False)