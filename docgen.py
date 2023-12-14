from llm import query_llm
from parser import parse_info, slot_fill
import json

def generate(listing, resume, output_pth = 'generated_letter_source/'):
    system_prompt = '''You are a cover letter writing assistant.  Only provide writing specifically requested.
    Do not speak to the user - just provide the needed writing.
    Be truthful and use details from the user’s resume to create an honest cover letter. Be extremely brief and succinct'''

    steps = [('prompt1.txt', 'prompt_1_example.json', 'sections/opening.tex'),
            ('prompt2.txt', 'prompt_2_example.json', 'sections/second.tex'),
            ('prompt3.txt', 'prompt_3_example.json', 'sections/closing.tex'),
            ('prompt4.txt', 'prompt_4_example.json', 'sections/signoff.tex')]

    prompts_pth = 'prompts/'
    examples_pth = 'examples/'


    for prompt, ex, out in steps:
        #get prompt and example
        with open(prompts_pth+prompt, 'r') as file:
            user_prompt = file.read()
        with open(examples_pth+ex, 'r') as file:
            chat_history = json.load(file)

        #get response paragraph
        paragraph, _ = query_llm(listing, resume, user_prompt, system_prompt, message_history = chat_history)

        #output response
        with open(output_pth+out, 'w') as file:
            file.write(paragraph)

def read_and_fill(listing, resume, output_pth = 'generated_letter_source/'):
    info = parse_info(listing, resume)

    cv = 'cover_letter.tex'

    with open(output_pth+cv, 'r') as file:
        doc = file.read()

    doc = slot_fill(doc, info)

    with open(output_pth+cv, 'w') as file:
        file.write(doc)
