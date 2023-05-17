import os
import openai
import re
import json
from dotenv import load_dotenv
load_dotenv()

token = os.environ.get("apikey")

story = ""
userInput = ""

ORDER = []
openai.api_key = token


def chat_with_gpt():
    global ORDER
    print("\nThinking...")
    prompt = '''With the additional prompt near the end of this 
                message and after the colon, create a madlibs that can be filled out later, 
                with exactly eight places where input is needed and exactly five sentences long. 
                Specify the types of words that need to be filled out 
                (adverb, verb, etc, but not name) by putting the word 
                type in parentheses where the word should go. Make the stories silly, 
                and make the inputs ambiguous so multiple words would work. Only output the 
                paragraph. Do not add anything before or afterwards: ''' + userInput
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who makes very funny madlibs for children."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    message = response['choices'][0]['message']['content']

    print("\nThinking some more...")
    newprompt = prompt + "\n " + message + '''\n
                If there are more than 10 places that need to be filled in, update the story to have less than 10 but more than 5.
                Now take that story and split it into a json array 
                where each element in the array is a sentence string split at the fill-in place or the fill-in object that will be provided later.  
                The element in the array should be in the same order as the places that need to be filled 
                in and each element that is a fill-in should have an json object that has the "type" associated with it, a default place fill-in word, and a description on what the type is.  
                The filled in spots should be split into the array as well, but as a string and in order amongst the fill-in objects.
                The resulting array should look like:
                [
                    "This is the first sentence.  It has no fill ins. My dog likes to ",
                    { // fill places are broken out into their own objects
                        "type": "verb",
                        "default": "run",
                        "description": "an action word"
                    },
                    ". This is the next sentence without fill ins or places.  And my cat likes to ",
                    { // fill ins are broken out into their own objects
                        "type": "verb",
                        "default": "sleep",
                        "description": "an action word"
                    },
                    ". Story conclusion.",
                    ...
                ]
                Return only the json array so that I can load it with json.loads in python, with nothing before or after.'''
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant who is an expert in json and python coding."},
            {"role": "user", "content": newprompt}
        ],
        max_tokens=2000
    )

    message = response['choices'][0]['message']['content']
    response = ""
    try:
        response = json.loads(message)
    except:
        print("Failed to parse json.  Trying again...", response)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who is an expert in json and python coding."},
                {"role": "user", "content": newprompt}
            ],
            max_tokens=2000
        )

        message = response['choices'][0]['message']['content']
        response = json.loads(message)

    return response


def check_with_gpt(word, type):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful yet laconic assistant."},
            {"role": "user", "content": "simply respond True or False to whether or not the first word after the colon is the type of word of the second word after the colon: " + word + " " + type}
        ],
    )
    message = response['choices'][0]['message']['content']
    if "true" in message.lower():
        return True
    else:
        return False


yourLibs = []

another = True
while another:
    userInput = input("What do you want the madlibs to be about? ")
    story = ""
    story = chat_with_gpt()
    wholeStory = ""
    count = 0
    for i in story:
        if not isinstance(i, str):
            count = count + 1

    print("There are " + str(count) +
          " words that need to be filled in. Press enter to take the default.")
    for i in story:
        if not isinstance(i, str):
            userWord = input(i["type"][0].upper() +
                             i["type"][1:]+" (Something like "+i["default"]+"): ")
            if (userWord == ""):
                userWord = i["default"]
            while not check_with_gpt(userWord, i["type"]):
                print("thats the wrong type")
                userWord = input("What would you like the word to be? (" + i["type"][0].upper() +
                                 i["type"][1:] + "):")
            wholeStory += userWord
        else:
            wholeStory += i

    print(wholeStory)
    yourLibs.append(story)
    playAgain = input(
        "\nWould you like to do another one (y/n)? You can also see all of your previous madlibs by typing \"print\": ")
    while playAgain == "print":
        for i in yourLibs:
            print(i+"\n\n\n\n")
        playAgain = input(
            "\nWould you like to do another one (y/n)? You can also see all of your previous madlibs by typing \"print\": ")
    if playAgain == "y":
        another = True
    else:
        another = False
