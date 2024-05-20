from transformers import pipeline
import torch
import gradio as gr
import json
from lang_codes import get_language_code, get_language_list

text_translator  = pipeline("translation", model="facebook/nllb-200-distilled-600M", torch_dtype=torch.bfloat16)

def translate_text(text, source = "English", target = "German"):
  src_code = get_language_code(source)
  dest_code = get_language_code(target)
  translation = text_translator(text, 
                                src_lang=src_code,
                                tgt_lang=dest_code)
  return translation[0]["translation_text"]

# translate_text("Hello Friends. How are you?", "German")

language_list = get_language_list()

gr.close_all()

demo = gr.Interface(
    fn=translate_text, 
    inputs=[
      gr.Textbox(label="Input text to Translate"),
      gr.Dropdown(label="Select Input Language", choices=language_list, value="English"), 
      gr.Dropdown(label="Select Output Language", choices=language_list, value="German"), 
            ], 
    outputs=[
        gr.Textbox(label="Translated text", lines=6)
        ], 
    title="Multi Language Translator", 
    description="This App translates from any language to any langauge")
demo.launch()





  