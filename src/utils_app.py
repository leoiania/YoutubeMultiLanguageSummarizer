import time

def button_timer(seconds=5):
    time.sleep(seconds)

def update_button(selected_language):
    # Update the button text when a new language is selected
    return f"Translate/Explain in {selected_language}"
