import os


def parse_questions(filename="questions.txt"):
  """Reads and parses questions.txt into a list of dictionaries."""
  if not os.path.exists(filename):
    print(f"Error: Could not find '{filename}' in the current directory.")
    return []

  questions = []
  current_q = None
  current_a = None

  with open(filename, "r", encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if not line:
        continue
      # Check if line starts with a number followed by a period (e.g., "1. ")
      if "." in line and line.split(".")[0].isdigit():
        if current_q and current_a:
          questions.append({"question": current_q, "answer": current_a})
        # Split number/question text
        parts = line.split(".", 1)
        current_q = parts[1].strip()
        current_a = None
      elif line.startswith("Answer:"):
        current_a = line.replace("Answer:", "", 1).strip()

    # Append the last question
    if current_q and current_a:
      questions.append({"question": current_q, "answer": current_a})

  return questions


def run_flashcards():
  filename = "questions.txt"
  deck = parse_questions(filename)

  if not deck:
    print("I didn't find that flashcard. Please make sure questions.txt exists and try again.")
    return

  print("=" * 60)
  print("🧠 CYBERSECURITY & AI GOVERNANCE FLASHCARD ENGINE")
  print(f"Loaded {len(deck)} questions from {filename}.")
  print("=" * 60)
  print("Instructions: Select 'Enter' to reveal the answer, then grade yourself.")
  print("Type 'q' at any prompt to quit early.\n")

  missed_cards = []

  for i, card in enumerate(deck, 1):
    print(f"\n[Card {i}/{len(deck)}]")
    print(f"Q: {card['question']}")

    user_input = input("\nPress [Enter] to see the answer (or 'q' to quit): ")
    if user_input.lower().strip() == "q":
      print("\nExiting session early. Keep up the great work!")
      return

    print(f"\nAnswer: {card['answer']}")
    print("-" * 60)

    result = (
        input("Did you get it correct? Type [y]es or [n]o: ").lower().strip()
    )
    if result == "n":
      missed_cards.append(card)
      print("-> Marked for review.")
    elif result == "y":
      print("-> Nailed it!")
    else:
      print("-> Unrecognized input, treating as incorrect for review.")
      missed_cards.append(card)

  # Review Loop for Missed Questions
  if missed_cards:
    print("\n" + "=" * 60)
    print(
        f"🔄 REVIEW ROUND: You missed {len(missed_cards)} question(s). Let's run"
        " through them!"
    )
    print("=" * 60)

    while missed_cards:
      card = missed_cards.pop(0)
      print(f"\nReview Q: {card['question']}")
      input("\nPress [Enter] to see the answer: ")
      print(f"\nAnswer: {card['answer']}")
      print("-" * 60)

      result = (
          input("Did you get it right this time? Type [y]es or [n]o: ").lower().strip()
      )
      if result != "y":
        print("-> Staying in the queue for another look.")
        missed_cards.append(card)
      else:
        print("-> Of course you did!, keep thriving!")

    print("\n✨ All missed cards successfully reviewed! Great job!")
  else:
    print(
        "\n🎉 Are you sure you needed to study? Incredible job!"
        " zero misses!"
    )


if __name__ == "__main__":
  run_flashcards()
