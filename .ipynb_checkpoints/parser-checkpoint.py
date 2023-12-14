from openai import OpenAI
import re

'''
LLM call for getting information out of a document.
'''
def parse(span, user_prompt):
    client = OpenAI()
    system_prompt = '''You are a parser that fetches the relevant data from a context.
    Return exactly what the user asks for and no other tokens.
    If what the user requests is not in the context, return '', an empty string. '''
    context = 'Context: ' + span + '\n'
    final_prompt = context + user_prompt

    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": final_prompt},
            ]
        )

    generation = response.choices[0].message.content

    return generation

'''
Gets a variety of needed information from a resume and listing using parse()
'''
def parse_info(listing, resume):
    get_name = 'Return the name of the person from this resume'
    get_email = 'Return the e-mail of the person from this resume'
    get_phone = 'Return the phone number of the person from this resume'
    get_title = 'Return the job title of the person from this resume'
    get_position = 'Return the name of the position offered in this job listing'
    get_company = 'Return the name of the company or organization that is offering this job listing.'

    name, email = parse(resume, get_name), parse(resume, get_email)
    number, title = parse(resume, get_phone), parse(resume, get_title)
    position, company = parse(listing, get_position), parse(listing, get_company)

    info = {'name':name, 'email':email, 'number':number, 'title':title,
           'position':position, 'company':company}
    return info

'''Function to add specific information to latex header'''
def slot_fill(doc, info):
    doc = re.sub(r"name\{First Last\}", "name{{{}}}".format(info['name']), doc)
    doc = re.sub(r"email\{email@email.com\}", "email{{{}}}".format(info['email']), doc)
    doc = re.sub(r"phone\{\(xxx\) xxx\-xxxx\}", "phone{{{}}}".format(info['number']), doc)
    doc = re.sub(r"role\{Data Scientist\}", "role{{{}}}".format(info['title']), doc)
    doc = re.sub(r"position\{Senior Data Scientist\}", "position{{{}}}".format(info['position']), doc)
    doc = re.sub(r"company\{Big Data\}", "company{{{}}}".format(info['company']), doc)
    return doc
