import json
import os
import random
import time


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
      if "." in line and line.split(".")[0].isdigit():
        if current_q and current_a:
          questions.append({"question": current_q, "answer": current_a})
        parts = line.split(".", 1)
        current_q = parts[1].strip()
        current_a = None
      elif line.startswith("Answer:"):
        current_a = line.replace("Answer:", "", 1).strip()

    if current_q and current_a:
      questions.append({"question": current_q, "answer": current_a})

  return questions


def save_progress_log(session_data, log_filename="flashcard_progress.json"):
  """Appends session performance data to a local JSON log file."""
  history = []
  if os.path.exists(log_filename):
    try:
      with open(log_filename, "r", encoding="utf-8") as f:
        history = json.load(f)
    except json.JSONDecodeError:
      history = []

  history.append(session_data)

  with open(log_filename, "w", encoding="utf-8") as f:
    json.dump(history, f, indent=4)
  print(f"\n📁 Session progress successfully saved to {log_filename}!")


def run_flashcards():
  filename = "questions.txt"
  deck = parse_questions(filename)

  if not deck:
    print("No flashcards found to review. Please make sure questions.txt exists.")
    return

  # Shuffle the deck randomly on each run
  random.shuffle(deck)

  print("=" * 60)
  print("🧠 CYBERSECURITY & AI GOVERNANCE FLASHCARD ENGINE + SHUFFLE")
  print(f"Loaded and shuffled {len(deck)} questions from {filename}.")
  print("=" * 60)
  print(
      "Instructions: Press Enter to reveal the answer, then grade yourself."
  )
  print("Type 'q' at any prompt to quit early.\n")

  missed_cards = []
  total_cards = len(deck)
  correct_first_try = 0
  card_timings = []

  session_start_time = time.time()

  for i, card in enumerate(deck, 1):
    print(f"\n[Card {i}/{total_cards}]")
    print(f"Q: {card['question']}")

    card_start_time = time.time()
    user_input = input("\nPress [Enter] to see the answer (or 'q' to quit): ")
    if user_input.lower().strip() == "q":
      print("\nExiting session early. Keep up the great work!")
      return

    card_elapsed = time.time() - card_start_time
    card_timings.append(card_elapsed)

    print(f"\nAnswer: {card['answer']}")
    print(
        f"⏱️  Time spent on card: {card_elapsed:.1f}s"
        " ────────────────────────"
    )

    result = (
        input("Did you get it right? Type [y]es or [n]o: ").lower().strip()
    )
    if result == "n":
      missed_cards.append(card)
      print("-> Marked for review. You've got this!")
    elif result == "y":
      correct_first_try += 1
      print("-> Nailed it! Of course you did, keep thriving!")
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
          input("Got it right this time? Type [y]es or [n]o: ").lower().strip()
      )
      if result != "y":
        print("-> Staying in the queue for another look.")
        missed_cards.append(card)
      else:
        print("-> Excellent, cleared from review!")

    print("\n✨ All missed cards successfully reviewed! Great job!")
  else:
    print(
        "\n🎉 Incredible job! You got every card right on the first try with"
        " zero misses!"
    )

  # Calculate final stats
  total_elapsed = time.time() - session_start_time
  score_percentage = (correct_first_try / total_cards) * 100
  avg_time_per_card = sum(card_timings) / total_cards

  print("\n" + "=" * 60)
  print("📊 SESSION PERFORMANCE SUMMARY")
  print("=" * 60)
  print(f"• Final Score: {score_percentage:.1f}% ({correct_first_try}/{total_cards} first-try correct)")
  print(f"• Total Session Time: {total_elapsed:.1f} seconds")
  print(f"• Average Time Per Card: {avg_time_per_card:.1f} seconds")
  print("=" * 60)

  # Package and save log
  session_data = {
      "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
      "total_cards": total_cards,
      "correct_first_try": correct_first_try,
      "score_percentage": round(score_percentage, 1),
      "total_duration_seconds": round(total_elapsed, 1),
      "avg_card_duration_seconds": round(avg_time_per_card, 1),
  }
  save_progress_log(session_data)


if __name__ == "__main__":
  run_flashcards()
