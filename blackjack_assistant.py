import tkinter as tk
from tkinter import ttk

# --- Blackjack Card Values and Logic ---

CARD_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

HI_LO_VALUES = {
    "2": +1, "3": +1, "4": +1, "5": +1, "6": +1,
    "7": 0, "8": 0, "9": 0,
    "10": -1, "J": -1, "Q": -1, "K": -1, "A": -1
}

STRATEGY = {
    8:   {2:"Hit",3:"Hit",4:"Hit",5:"Hit",6:"Hit",7:"Hit",8:"Hit",9:"Hit",10:"Hit",11:"Hit"},
    9:   {2:"Hit",3:"Double Down",4:"Double Down",5:"Double Down",6:"Double Down",7:"Hit",8:"Hit",9:"Hit",10:"Hit",11:"Hit"},
    10:  {2:"Double Down",3:"Double Down",4:"Double Down",5:"Double Down",6:"Double Down",7:"Double Down",8:"Double Down",9:"Double Down",10:"Hit",11:"Hit"},
    11:  {2:"Double Down",3:"Double Down",4:"Double Down",5:"Double Down",6:"Double Down",7:"Double Down",8:"Double Down",9:"Double Down",10:"Double Down",11:"Hit"},
    12:  {2:"Hit",3:"Hit",4:"Stand",5:"Stand",6:"Stand",7:"Hit",8:"Hit",9:"Hit",10:"Hit",11:"Hit"},
    13:  {2:"Stand",3:"Stand",4:"Stand",5:"Stand",6:"Stand",7:"Hit",8:"Hit",9:"Hit",10:"Hit",11:"Hit"},
    14:  {2:"Stand",3:"Stand",4:"Stand",5:"Stand",6:"Stand",7:"Hit",8:"Hit",9:"Hit",10:"Hit",11:"Hit"},
    15:  {2:"Stand",3:"Stand",4:"Stand",5:"Stand",6:"Stand",7:"Hit",8:"Hit",9:"Surrender",10:"Surrender",11:"Hit"},
    16:  {2:"Stand",3:"Stand",4:"Stand",5:"Stand",6:"Stand",7:"Surrender",8:"Surrender",9:"Surrender",10:"Surrender",11:"Surrender"},
    17:  {2:"Stand",3:"Stand",4:"Stand",5:"Stand",6:"Stand",7:"Stand",8:"Stand",9:"Stand",10:"Stand",11:"Stand"},
}

def calculate_hand_value(cards):
    total = 0
    aces = 0
    for c in cards:
        if c == "A":
            aces += 1
        else:
            total += CARD_VALUES.get(c, 0)
    for _ in range(aces):
        if total + 11 <= 21:
            total += 11
        else:
            total += 1
    return total

def calculate_running_count(cards):
    count = 0
    for c in cards:
        count += HI_LO_VALUES.get(c, 0)
    return count

def best_move(player_total, dealer_up):
    if player_total >= 17:
        return "Stand"
    if player_total < 8:
        return "Hit"
    dealer_up_val = dealer_up
    if dealer_up_val > 11:
        dealer_up_val = 11
    moves = STRATEGY.get(player_total)
    if moves:
        return moves.get(dealer_up_val, "Hit")
    return "Hit"

# --- GUI Frames ---

class HandFrame(ttk.Frame):
    def __init__(self, parent, hand_num):
        super().__init__(parent)
        self.hand_num = hand_num
        ttk.Label(self, text=f"Hand {hand_num+1}:").grid(row=0, column=0, padx=5)
        self.card_vars = []
        self.card_boxes = []
        for i in range(5):
            var = tk.StringVar()
            cb = ttk.Combobox(self, textvariable=var, width=3, values=list(CARD_VALUES.keys()))
            cb.grid(row=0, column=i+1, padx=2)
            self.card_vars.append(var)
            self.card_boxes.append(cb)

    def get_all_cards(self):
        cards = []
        for var in self.card_vars:
            val = var.get().strip().upper()
            if val in CARD_VALUES:
                cards.append(val)
        return cards

    def clear(self):
        for var in self.card_vars:
            var.set("")

class DealerFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        ttk.Label(self, text="Dealer Cards:").grid(row=0, column=0, padx=5)
        self.card_vars = []
        self.card_boxes = []
        for i in range(5):
            var = tk.StringVar()
            cb = ttk.Combobox(self, textvariable=var, width=3, values=list(CARD_VALUES.keys()))
            cb.grid(row=0, column=i+1, padx=2)
            self.card_vars.append(var)
            self.card_boxes.append(cb)

    def get_all_cards(self):
        cards = []
        for var in self.card_vars:
            val = var.get().strip().upper()
            if val in CARD_VALUES:
                cards.append(val)
        return cards

    def clear(self):
        for var in self.card_vars:
            var.set("")

# --- Main Blackjack Advisor App ---

class BlackjackAdvisorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Blackjack Advisor with Card Counting")
        self.geometry("850x400")
        self.resizable(False, False)

        self.all_seen_cards = []
        self.hands = []

        self.hands_frame = ttk.Frame(self)
        self.hands_frame.pack(pady=10)

        self.dealer_frame = DealerFrame(self)
        self.dealer_frame.pack(pady=5)

        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        self.add_hand_btn = ttk.Button(btn_frame, text="Add Hand", command=self.add_hand)
        self.add_hand_btn.grid(row=0, column=0, padx=5)

        self.new_hand_btn = ttk.Button(btn_frame, text="New Hand (Clear Inputs)", command=self.clear_all)
        self.new_hand_btn.grid(row=0, column=1, padx=5)

        self.new_shoe_btn = ttk.Button(btn_frame, text="New Shoe (Reset Count)", command=self.reset_shoe)
        self.new_shoe_btn.grid(row=0, column=2, padx=5)

        self.advice_btn = ttk.Button(btn_frame, text="Get Advice", command=self.get_advice)
        self.advice_btn.grid(row=0, column=3, padx=5)

        self.output = tk.Text(self, height=10, width=100)
        self.output.pack(pady=10)

        self.add_hand()

    def add_hand(self):
        hand_frame = HandFrame(self.hands_frame, len(self.hands))
        hand_frame.pack(pady=5)
        self.hands.append(hand_frame)

    def clear_all(self):
        for hand in self.hands:
            hand.clear()
        self.dealer_frame.clear()

    def reset_shoe(self):
        self.clear_all()
        self.all_seen_cards = []
        self.output.delete(1.0, tk.END)
        self.output.insert(tk.END, "New shoe started. Running count reset.\n")

    def get_advice(self):
        self.output.delete(1.0, tk.END)
        dealer_cards = self.dealer_frame.get_all_cards()
        dealer_value = calculate_hand_value(dealer_cards)
        dealer_bust = dealer_value > 21

        current_cards = dealer_cards.copy()
        advice_lines = []

        if dealer_bust:
            advice_lines.append(f"Dealer busts with total {dealer_value}!")

        for i, hand in enumerate(self.hands):
            cards = hand.get_all_cards()
            if not cards:
                advice_lines.append(f"Hand {i+1}: No cards entered.")
                continue
            hand_value = calculate_hand_value(cards)
            busted = hand_value > 21

            current_cards.extend(cards)
            move = best_move(hand_value, dealer_value if dealer_value <= 11 else 11)

            advice_lines.append(f"Hand {i+1}: Cards {cards} Total={hand_value} → Move: {move} {'(Busted)' if busted else ''}")

        self.all_seen_cards.extend(current_cards)

        running_count = calculate_running_count(self.all_seen_cards)
        advice_lines.append(f"\nRunning Count: {running_count}")

        self.output.insert(tk.END, "\n".join(advice_lines))


if __name__ == "__main__":
    app = BlackjackAdvisorApp()
    app.mainloop()
