import openai
import re
story = ""
userInput = ""

ORDER = []
openai.api_key = "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"






def chat_with_gpt():
    global ORDER
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "With the additional prompt near the end of this message and after the colon, create a mad libs that can be filled out later, with exactly eight places where input is needed and exactly five sentances long. Specify the types of words that need to be filled out (adverb, verb, etc, but not name) by putting the word type in parentheses where the word should go. Do your best to make the stories silly, and make the inputs ambiguous so multiple words would work. Only output the paragraph. Do not add anything before or afterwards: " + userInput}
        ],
        max_tokens=500
    )
    message = response['choices'][0]['message']['content']
    # Extract the word types from the message using regex
    ORDER = re.findall(r'\((.*?)\)', message)
    
    return message







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
    






def regenerate(story):
    global ORDER
    global userInput
    supposedContent = "With the additional prompt near the end of this message and after the colon, create a mad libs that can be filled out later, with exactly eight places where input is needed and exactly five sentances long. Specify the types of words that need to be filled out (adverb, verb, etc, but not name) by putting the word type in parentheses where the word should go. Do your best to make the stories silly, and make the inputs ambiguous so multiple words would work. Only output the paragraph. Do not add anything before or afterwards: " + userInput + "\". Rewrite the paragraph, but fill exactly five of the input places with words of your own. Ensure that there are still more than five spots remaining afterwards: "+ story
    print(supposedContent)
    print("\n\n\n\n")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": supposedContent}
        ],
        max_tokens=500
    )
    message = response['choices'][0]['message']['content']
    ORDER = re.findall(r'\((.*?)\)', message)
    return message










yourLibs = []

another = True
while another:
    userInput = input("What do you want the madlibs to be about? ")
    story = ""
    ORDER = []
    story = chat_with_gpt()
    while len(ORDER) > 15 or len(ORDER) < 5:
        ORDER = []
        story = regenerate(story)
        print(len(ORDER))
        print(story)
        print("\n\n\n\n")

    print("Number of openings: "+str(len(ORDER)))
    for i in ORDER:
        dataFind = "("+i+")"
        userWord = input(i[0].upper()+i[1:]+": ")
        while not check_with_gpt(userWord, i):
            print("thats the wrong type")
            userWord = input("What would you like the word to be?")
        story = story.replace(dataFind, userWord,1)
    print(story)
    yourLibs.append(story)
    playAgain = input("Would you like to do another one (y/n)? You can also see all of your previous madlibs by typing \"print\": ")
    while playAgain == "print":
        for i in yourLibs:
            print(i+"\n\n\n\n")
        playAgain = input("Would you like to do another one (y/n)? You can also see all of your previous madlibs by typing \"print\": ")
    if playAgain == "y":
        another = True
    else:
        another = False