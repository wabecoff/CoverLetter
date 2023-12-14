from openai import OpenAI

def extract_score(text):
    # Find the index of 'SCORE:'
    score_idx = text.find('SCORE:')
    if score_idx == -1:
        return None  # 'SCORE:' not found in the string

    # Extract the substring after 'SCORE:'
    substring_after_score = text[score_idx + len('SCORE:'):]

    # Extract the number from the substring
    for word in substring_after_score.split():
        if word.isdigit():
            return int(word)
    return None  # No number found after 'SCORE:'

def duo_score(source, response, criterion):
    client = OpenAI()

    system_prompt = '''You are a scoring program.  Given a criteria and source and response you will output a score from 1 to 100.
    Explicitly explain your reasoning, and then finally output a score.  Your response should look like
    EXPLANATION: (A few sentences describing the response in terms of the criteria and the source)
    SCORE: {some score 1-100}
    '''

    final_prompt = 'CRITERIA: ' + criterion + '\nSOURCE: ' + source + '\nRESPONSE: ' + response +'\nEXPLANATION: '

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt},
            ]
        )

    generation = response.choices[0].message.content

    return extract_score(generation), generation


def score(text, criterion):
    client = OpenAI()

    system_prompt = '''You are a scoring program.  Given a criteria and an input you will output a score from 1 to 100.
    Explicitly explain your reasoning, and then finally output a score.  Your response should look like
    EXPLANATION: (A few sentences describing the input in terms of the criteria)
    SCORE: {some score 1-100}
    '''

    final_prompt = 'CRITERIA: ' + criterion + '\nINPUT: ' + text + '\nEXPLANATION: '

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt},
            ]
        )

    generation = response.choices[0].message.content #usage as of Dec 2023

    return extract_score(generation), generation

def formality(text):
    criteria = '''Score this input on formality where 1 is least formal and 100 is most formal.
    You are evaluating for formality in style and content.'''
    return score(text, criteria)

def quality(text):
    criteria = '''Score this input on quality where 1 is lowest quality and 100 is highest quality.
    You are evaluating for quality in terms of persuasiveness and style.'''
    return score(text, criteria)

def relevance(source, response):
    criteria = '''Score this response in terms of relevance to the source where 1 is least relevant and 100 is most relevant.'''
    return duo_score(source, response, criteria)

def groundedness(source, response):
    criteria = '''Score this response in terms of groundedness to the source where 1 is least grounded and 100 is most grounded.
    Reponses that make claims that can not be supported by the source have lower groundedness.'''
    return duo_score(source, response, criteria)

def score_report(generation, listing, resume, verbose = False):
    cur_quality, _ = quality(generation)
    if verbose: print('Quality Score: ', cur_quality)
    cur_formality, _ = formality(generation)
    if verbose: print('Formality Score: ', cur_formality)
    cur_relevance, _ = relevance(listing, generation)
    if verbose: print('Relevance Score: ', cur_relevance)
    cur_groundedness, _ = groundedness(resume, generation)
    if verbose: print('Groundedness Score: ', cur_groundedness)

    final_score = sum([cur_quality, cur_formality, cur_relevance, cur_groundedness])
    if verbose: print('Total: ', final_score)
    return final_score
