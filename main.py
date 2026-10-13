from deep_translator import GoogleTranslator

print("English to Tamil Translator")
print("---------------------------")

while True:
    text = input("\nEnter English text (or type 'exit' to quit): ")

    if text.lower() == "exit":
        print("Translator closed!")
        break

    try:
        translated_text = GoogleTranslator(
            source="en",
            target="ta"
        ).translate(text)

        print("Tamil Translation:", translated_text)

    except Exception as e:
        print("Translation failed. Please check your internet connection.")