from openai import OpenAI

'''
Takes in a job listing, resume, and prompts that controll what the agent generates.
Outputs generation as well as message history.
We can also a message history for few-shot prompting functionality.
'''
def query_llm(listing, resume, user_prompt, system_prompt, message_history = []):
    client = OpenAI()

    listing_prompt = 'LISTING: ' + listing + '\n'
    resume_prompt = 'RESUME: ' + resume + '\n'
    final_prompt = listing_prompt + resume_prompt + user_prompt

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=message_history + [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt},
            ]
        )

    generation = response.choices[0].message.content #usage as of Dec 2023

    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": final_prompt},
        {"role": "assistant", "content": generation},
    ]

    return generation, messages


'''
Used to generate examples for few-shot learning.
Examples are generated with base prompt and ranked with an arbitrary scoring function.
'''
def annotate_examples(listings, resumes, user_prompt, system_prompt, score_fn, top_k=2):
    scored_histories = []

    # Iterate over each listing and resume pair
    for listing, resume in zip(listings, resumes):
        # Get the generation and message history from query_llm
        generation, message_history = query_llm(listing, resume, user_prompt, system_prompt)

        # Score the generation
        score = score_fn(generation, listing, resume)

        # Add the score and the message history to the list
        scored_histories.append((score, message_history))

    # Sort the list by score in descending order
    scored_histories.sort(key=lambda x: x[0], reverse=True)

    # Extract the message histories of the top k examples
    top_k_histories = [history for _, history in scored_histories[:top_k]]

    return top_k_histories
