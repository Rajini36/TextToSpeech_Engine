from tts import TextToSpeech

tts=TextToSpeech()
print("=== Text to Speech Engine ===")
print("Type 'exit' to quit.\n")
while True:
    text=input("Enter Text: ")
    if text.lower()=="exit":
        print("Goodbye!")
        break
    tts.speak(text)
    