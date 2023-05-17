import openai
ORDER = []
openai.api_key = "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"


def chat_with_gpt(prompt):
    global ORDER
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    message = response['choices'][0]['message']['content']
    prompt = "now give me the order in which the words that have to be filled out are in, with parenthesis, just like they are shown in the text. do this in the form of a list \"[wordtype1,wordtype2]\""
    ORDER = response['choices'][1]['message']['content']

    return message



userInput = input("What do you want the madlibs to be about? ")

print(chat_with_gpt("""With the additional prompt near the end of this message and after the colon, create a mad libs that can be filled out later, with exactly 7 spots where input is needed. Specify the types of words that need to be filled out (adverb, verb, etc, but not name) by putting them in parenthesis where the word should go. Do your best to make the stories silly!:"""+userInput))

print(ORDER)