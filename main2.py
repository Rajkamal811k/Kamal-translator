from translate import Translator

translator = Translator(from_lang="en", to_lang="ta")

print("English to Tamil Translator")
print("---------------------------")

while True:
    text = input("\nEnter English text (or type 'exit' to quit): ").strip()

    if text.lower() == "exit":
        print("Translator closed!")
        break

    if not text:
        print("Please enter some text.")
        continue

    try:
        result = translator.translate(text)
        print("Tamil Translation:", result)

    except Exception as e:
        print("Translation failed:", e)