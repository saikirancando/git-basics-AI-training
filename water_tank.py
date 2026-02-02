"""
WATER TANK

This file is a standalone version of the game. It includes:
- deck setup and dealing
- `use_card`, `apply_overflow`
- `human_play` and deterministic `computer_play`
- `main()` entrypoint

Run with: python3 water_tank.py
"""

import random

TANK_TARGET = 80


def setup_cards():
    """Create shuffled water and power piles."""
    water_cards_pile = (
        [1] * 10 + [2] * 10 + [3] * 10 + [4] * 8 + [5] * 8 + [10] * 6 + [15] * 4
    )
    power_cards_pile = ["DOT"] * 8 + ["SOH"] * 6 + ["DMT"] * 4
    random.shuffle(water_cards_pile)
    random.shuffle(power_cards_pile)
    return water_cards_pile, power_cards_pile


def arrange_hand(cards):
    water_sorted = sorted([c for c in cards if isinstance(c, int)])
    power_sorted = sorted([c for c in cards if isinstance(c, str)])
    cards[:] = water_sorted + power_sorted


def deal_cards(water_cards_pile, power_cards_pile, water_each=3, power_each=2):
    human = []
    computer = []
    for _ in range(water_each):
        if water_cards_pile:
            human.append(water_cards_pile.pop())
        if water_cards_pile:
            computer.append(water_cards_pile.pop())
    for _ in range(power_each):
        if power_cards_pile:
            human.append(power_cards_pile.pop())
        if power_cards_pile:
            computer.append(power_cards_pile.pop())
    arrange_hand(human)
    arrange_hand(computer)
    return human, computer


def draw_same_type_card(card_used_or_discarded, water_cards_pile, power_cards_pile):
    if isinstance(card_used_or_discarded, int):
        return water_cards_pile.pop() if water_cards_pile else None
    else:
        return power_cards_pile.pop() if power_cards_pile else None


def apply_overflow(tank):
    return min(tank, TANK_TARGET)


def use_card(player_tank, chosen_card, player_hand, opponent_tank):
    if chosen_card in player_hand:
        player_hand.remove(chosen_card)
    if isinstance(chosen_card, int):
        player_tank += chosen_card
    elif chosen_card == "DOT":
        pass
    elif chosen_card == "SOH":
        steal = min(5, opponent_tank)
        opponent_tank -= steal
        player_tank += steal
    elif chosen_card == "DMT":
        player_tank += 10
    player_tank = apply_overflow(player_tank)
    opponent_tank = apply_overflow(opponent_tank)
    return player_tank, opponent_tank


def human_play(human_tank, human_hand, water_cards_pile, power_cards_pile, computer_tank):
    print("\n===== Human player's turn =====")
    print(f"Your water level: {human_tank}")
    print(f"Computer water level: {computer_tank}")
    print("\nYour hand:")
    for i, c in enumerate(human_hand, start=1):
        print(f"  {i}. {c}")
    while True:
        action = input("\nEnter a card number to USE, or D to DISCARD: ").strip().lower()
        if action == "d":
            if not human_hand:
                print("You have no cards to discard.")
                continue
            idx_str = input("Enter the card number to discard: ").strip()
            if not idx_str.isdigit():
                print("Please enter a valid number.")
                continue
            idx = int(idx_str)
            if not (1 <= idx <= len(human_hand)):
                print("Out of range.")
                continue
            discarded = human_hand.pop(idx - 1)
            print(f"You discarded: {discarded}")
            new_card = draw_same_type_card(discarded, water_cards_pile, power_cards_pile)
            if new_card is not None:
                human_hand.append(new_card)
            arrange_hand(human_hand)
            print(f"Updated levels -> You: {human_tank} | Computer: {computer_tank}")
            return human_tank, computer_tank
        if not action.isdigit():
            print("Enter a valid number or D.")
            continue
        idx = int(action)
        if not (1 <= idx <= len(human_hand)):
            print("Out of range.")
            continue
        chosen_card = human_hand[idx - 1]
        print(f"You used: {chosen_card}")
        human_tank, computer_tank = use_card(human_tank, chosen_card, human_hand, computer_tank)
        new_card = draw_same_type_card(chosen_card, water_cards_pile, power_cards_pile)
        if new_card is not None:
            human_hand.append(new_card)
        arrange_hand(human_hand)
        print(f"Updated levels -> You: {human_tank} | Computer: {computer_tank}")
        return human_tank, computer_tank


def simulate_card_effect(player_tank, card, opponent_tank):
    comp = player_tank
    opp = opponent_tank
    if isinstance(card, int):
        comp += card
    elif card == "DOT":
        pass
    elif card == "SOH":
        steal = min(5, opp)
        opp -= steal
        comp += steal
    elif card == "DMT":
        comp += 10
    comp = apply_overflow(comp)
    opp = apply_overflow(opp)
    return comp, opp


def computer_play(computer_tank, computer_cards, water_cards_pile, power_cards_pile, opponent_tank):
    print("\n==========Computer Player's turn=====")
    print("Computer's water level is at {}".format(computer_tank))
    print("Your water level is at {}".format(opponent_tank))
    best_card = None
    best_score = None
    for card in computer_cards:
        sim_comp, sim_opp = simulate_card_effect(computer_tank, card, opponent_tank)
        type_pref = 1 if isinstance(card, str) else 0
        if isinstance(card, int):
            tie_val = card
        else:
            tie_val = {"DMT": 3, "SOH": 2, "DOT": 1}.get(card, 0)
        score = (sim_comp, -sim_opp, type_pref, tie_val)
        if best_score is None or score > best_score:
            best_score = score
            best_card = card
    if best_card is None:
        print("Computer has no card to play.")
        print("Computer's water level is at {}".format(computer_tank))
        print("Your water level is at {}".format(opponent_tank))
        return computer_tank, opponent_tank
    print("Computer playing with card: {}".format(best_card))
    computer_tank, opponent_tank = use_card(computer_tank, best_card, computer_cards, opponent_tank)
    computer_tank = apply_overflow(computer_tank)
    opponent_tank = apply_overflow(opponent_tank)
    new_card = draw_same_type_card(best_card, water_cards_pile, power_cards_pile)
    if new_card is not None:
        computer_cards.append(new_card)
    arrange_hand(computer_cards)
    print("Computer's water level is now {}".format(computer_tank))
    print("Your water level is now {}".format(opponent_tank))
    return computer_tank, opponent_tank


def main():
    print(
        "Welcome to the WATER TANK game and play against the computer!"
        "\nFill your tank by using or discarding a card for each turn."
        "\nThe first player to fill their tank wins the game. Good luck!"
    )
    human_tank = 0
    computer_tank = 0
    water_cards_pile, power_cards_pile = setup_cards()
    human_hand, computer_hand = deal_cards(water_cards_pile, power_cards_pile)
    turn = random.choice(["Human player", "Computer player"])
    print("\nThe", turn, "has been selected to go first")
    while human_tank < TANK_TARGET and computer_tank < TANK_TARGET:
        if turn == "Human player":
            human_tank, computer_tank = human_play(
                human_tank, human_hand, water_cards_pile, power_cards_pile, computer_tank
            )
            turn = "Computer player"
        else:
            computer_tank, human_tank = computer_play(
                computer_tank, computer_hand, water_cards_pile, power_cards_pile, human_tank
            )
            turn = "Human player"
    print("\n==== Game Over ====")
    if human_tank >= TANK_TARGET and computer_tank >= TANK_TARGET:
        print("It's a tie!")
    elif human_tank >= TANK_TARGET:
        print("Human player wins!")
    else:
        print("Computer player wins!")
    print(f"Final levels -> Human: {human_tank} | Computer: {computer_tank}")


if __name__ == "__main__":
    main()
