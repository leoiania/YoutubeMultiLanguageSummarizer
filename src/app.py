import gradio as gr
from main import PolySummaryYT
from utils_app import button_timer, update_button


TRANSLATOR = PolySummaryYT()
LANGUAGES_LIST = TRANSLATOR.get_languages()

CUSTOM_CSS_PATH = "styles.css"

def translate_click_start(youtube_url, language, groq_key, openai_key):
    result_translation = TRANSLATOR.summarize_video(youtube_url, language, groq_key, openai_key)
    return result_translation["audio_path"], result_translation["text"]


with gr.Blocks(css=CUSTOM_CSS_PATH) as iface:
    gr.Markdown(
    """
    # PolySummaryYT 🌐
    Summarize YouTube videos in any desired language
    """
    )

    with gr.Column(elem_classes="main-container"):
        groq_key_input = gr.Textbox(label="Enter your GROQ API KEY here! (Used for transcription and translation)", type="password")
        openai_key_input = gr.Textbox(label="Enter your OPENAI API KEY here! (Used for Text-to-Speech) - leave it empty for free text to speech model usage", type="password", placeholder="Leave it empty for free text to speech model usage")
    
    with gr.Column(elem_classes="main-container"):
        youtube_url = gr.Textbox(label="Enter YouTube URL")
        language = gr.Dropdown(
            choices= LANGUAGES_LIST,
            label= "Select language",
            value= LANGUAGES_LIST[0],
            interactive=True
        )
        translate_btn = gr.Button(f"Translate/Explain in {language.value}", elem_id="translate-btn")
       
    with gr.Column(elem_classes="output-container"):
        audio_output = gr.Audio(label="Translated Audio")
        result_text = gr.Textbox(label="Translation Result", interactive=False, elem_classes="result-text")
        
        language.change(
            update_button,  # to update button label
            inputs=language,  
            outputs=translate_btn 
        )
        #use the lambda funcion together with the "then" method in order to block the translate for 5 seconds after the request.
        translate_btn.click(fn=lambda: gr.update(interactive=False), inputs=None, outputs=translate_btn).then(
                            fn=translate_click_start, inputs=[youtube_url, language, groq_key_input, openai_key_input], outputs=[audio_output, result_text]).then(
                            fn=button_timer, inputs=None, outputs=None).then(
                            fn=lambda: gr.update(interactive=True), inputs=None, outputs=translate_btn)

if __name__ == "__main__":
    iface.launch(share=False)