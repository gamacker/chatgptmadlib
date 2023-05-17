import openai
import re

openai.api_key = "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"

def chat_with_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    message = response['choices'][0]['message']['content']
    return message

def expand_story(story):
    expanded_story = chat_with_gpt("Continue the following story but keep the same number of blanks: " + story)
    return expanded_story

def refine_story(story):
    refined_story = chat_with_gpt("Make the following story more interesting and funny: " + story)
    return refined_story

def extract_blanks_and_truncate_story(story, num_blanks):
    word_types = re.findall(r'\((.*?)\)', story)
    if len(word_types) < num_blanks:
        return story, word_types
    trunc_story = ''
    start_idx = 0
    for _ in range(num_blanks):
        end_idx = story.find(')', start_idx)
        trunc_story += story[start_idx:end_idx+1]
        start_idx = end_idx + 1
    return trunc_story, word_types[:num_blanks]

while True:
    userInput = input("What do you want the madlibs to be about? ")
    story = chat_with_gpt("""With the additional prompt near the end of this message and after the colon, create a mad libs that can be filled out later. Specify the types of words that need to be filled out (adverb, verb, etc, but not name) by putting the word type in parentheses where the word should go. Do your best to make the stories silly! Please also do not have a header or anything, simply go directly into the madlib: """ + userInput)
    story, word_types = extract_blanks_and_truncate_story(story, 10)
    story = expand_story(story)
    story = refine_story(story)
    print("Final Story:")
    print(story)
    print("Order of Word Types:")
    print(word_types)
    
    for i in word_types:
        dataFind = "("+i+")"
        userWord = input(i[0].upper()+i[1:]+": ")
        story = story.replace(dataFind, userWord,1)
    print(story)
    playAgain = input("Would you like to do another one (y/n)? ")
    if playAgain.lower() != 'y':
        break
