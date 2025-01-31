import tkinter as tk
from functools import partial
import random
from enum import IntEnum

# myRouletteGame by jjjk45 01.30.2025.23.48
# TODO:  put labels in the 1to18 row so that buttons can be perfectly aligned,
#       create a loop that uses a dictionary to generate buttons at runtime instead of having them all written out individually,
#       add more types of bets (2 & 3 number bets),

# create window
root = tk.Tk()
root.geometry("485x250")

# bet, chips, & spinresult variables
bet = tk.IntVar(value=0)
chips = tk.IntVar(value=1000)
spinResult = tk.IntVar(value=None)
payoutResult = tk.IntVar(value=0)


# pop up for when you run out of chips
def outOfChipsAlert():
    popUp = tk.Toplevel()
    popUp.grab_set()
    popUp.configure(bg="black")
    popUp.title = "Pop Up"
    popUpText = tk.Label(
        popUp,
        text="You Are Out of Chips!!!",
        font=("Times New Roman", 16),
        fg="white",
        bg="black",
    )
    popUpText.grid(row=0, column=0, padx=40, pady=5)
    popUpButton = tk.Button(
        popUp,
        text="Reset Chips?",
        bg="red",
        command=lambda: [popUpButtonHelper(), popUp.destroy()],
    )
    popUpButton.grid(row=1, column=0, padx=40, pady=5)
    return


# couldn't consolidate into one function because popUp is a local variable
def popUpButtonHelper():
    chips.set(1000)
    chipsDisplay.set("Chips: $1000")
    return


# function that controls last roll result counter in bottom right
def changePayoutResult(int):
    payoutResult.set(int)
    if payoutResult.get() >= 1:
        payoutResultDisplay.set("+" + str(payoutResult.get()))
        payoutResultLabel.configure(bg="lime")
    else:
        payoutResultDisplay.set(str(payoutResult.get()))
        payoutResultLabel.configure(bg="red")
    return


# bet change command for bet buttons
def changeBet(int):
    bet.set(value=int)
    betDisplay.set("Bet: $" + str(bet.get()))
    return


# simulating roulette wheel for single number & straight bets
def spinstraight(left, right):
    spin = random.randint(0, 36)
    spinResult.set(spin)
    return left <= spin <= right


# simulating roulette wheel for even/odd & column bets
def spinremainder(hit, divisor):
    spin = random.randint(0, 36)
    spinResult.set(spin)
    if spin == 0:
        return False
    return spin % divisor == hit


# simulating roulette wheel for color bets
def spincolor(color):
    red = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
    spin = random.randint(0, 36)
    spinResult.set(spin)
    if spin == 0:
        return False
    return (color == 0 and spin in red) or (not color == 0 and not spin in red)


# payout function
def payout(
    spintype, odds, one, two
):  # spintype is for determining function & the odds determine the payout
    # uses dictionary
    spin_checks = {
        1: lambda: spinstraight(one, two),
        2: lambda: spinremainder(one, two),
        3: lambda: spincolor(one),
    }
    spin_check = spin_checks.get(spintype)
    if spin_check and spin_check():
        chips.set(chips.get() + bet.get() * odds + bet.get())
        changePayoutResult(bet.get() * odds + bet.get())
    else:
        chips.set(chips.get() - bet.get())
        if chips.get() <= 0:
            outOfChipsAlert()
        changePayoutResult(bet.get() * -1)
    chipsDisplay.set("Chips: $" + str(chips.get()))
    spinDisplay.set("Roll: " + str(spinResult.get()))
    return


# enum class for increasing button readability in regards to roulette spintype (st is short for spintype)
# is it overkill to use enums AND a dictionary?
class st(IntEnum):
    spinStraight = 1
    spinRemainder = 2
    spinColor = 3


# 0-36 Button Frame (shortened to f1)
f1 = tk.Frame(root, bg="sea green", borderwidth=0)
f1.grid(row=0, column=0, sticky="ew")
# side green buttons
g0 = tk.Button(
    f1,
    text="0",
    bg="green",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 0, 0),
)
g0.grid(row=1, column=0, padx=5, pady=5)
gRow0 = tk.Button(
    f1,
    text="2 to 1",
    bg="green",
    fg="white",
    command=partial(payout, st.spinRemainder, 2, 0, 3),
)
gRow0.grid(row=0, column=13, padx=5, pady=5)
gRow1 = tk.Button(
    f1,
    text="2 to 1",
    bg="green",
    fg="white",
    command=partial(payout, st.spinRemainder, 2, 2, 3),
)
gRow1.grid(row=1, column=13, padx=5, pady=5)
gRow2 = tk.Button(
    f1,
    text="2 to 1",
    bg="green",
    fg="white",
    command=partial(payout, st.spinRemainder, 2, 1, 3),
)
gRow2.grid(row=2, column=13, padx=5, pady=5)
# red&black number buttons
r3 = tk.Button(
    f1,
    text="3",
    bg="red",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 3, 3),
)
r3.grid(row=0, column=1, padx=5, pady=5)
b2 = tk.Button(
    f1,
    text="2",
    bg="black",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 2, 2),
)
b2.grid(row=1, column=1, padx=5, pady=5)
r1 = tk.Button(
    f1,
    text="1",
    bg="red",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 1, 1),
)
r1.grid(row=2, column=1, padx=5, pady=5)
b6 = tk.Button(
    f1,
    text="6",
    bg="black",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 6, 6),
)
b6.grid(row=0, column=2, padx=5, pady=5)
r5 = tk.Button(
    f1,
    text="5",
    bg="red",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 5, 5),
)
r5.grid(row=1, column=2, padx=5, pady=5)
b4 = tk.Button(
    f1,
    text="4",
    bg="black",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 4, 4),
)
b4.grid(row=2, column=2, padx=5, pady=5)
r9 = tk.Button(
    f1,
    text="9",
    bg="red",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 9, 9),
)
r9.grid(row=0, column=3, padx=5, pady=5)
b8 = tk.Button(
    f1,
    text="8",
    bg="black",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 8, 8),
)
b8.grid(row=1, column=3, padx=5, pady=5)
r7 = tk.Button(
    f1,
    text="7",
    bg="red",
    fg="white",
    width=2,
    command=partial(payout, st.spinStraight, 35, 7, 7),
)
r7.grid(row=2, column=3, padx=5, pady=5)
r12 = tk.Button(
    f1,
    text="12",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 12, 12),
)
r12.grid(row=0, column=4, padx=5, pady=5)
b11 = tk.Button(
    f1,
    text="11",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 11, 11),
)
b11.grid(row=1, column=4, padx=5, pady=5)
b10 = tk.Button(
    f1,
    text="10",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 10, 10),
)
b10.grid(row=2, column=4, padx=5, pady=5)
b15 = tk.Button(
    f1,
    text="15",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 15, 15),
)
b15.grid(row=0, column=5, padx=5, pady=5)
r14 = tk.Button(
    f1,
    text="14",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 14, 14),
)
r14.grid(row=1, column=5, padx=5, pady=5)
b13 = tk.Button(
    f1,
    text="13",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 13, 13),
)
b13.grid(row=2, column=5, padx=5, pady=5)
r18 = tk.Button(
    f1,
    text="18",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 18, 18),
)
r18.grid(row=0, column=6, padx=5, pady=5)
b17 = tk.Button(
    f1,
    text="17",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 17, 17),
)
b17.grid(row=1, column=6, padx=5, pady=5)
r16 = tk.Button(
    f1,
    text="16",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 16, 16),
)
r16.grid(row=2, column=6, padx=5, pady=5)
r21 = tk.Button(
    f1,
    text="21",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 21, 21),
)
r21.grid(row=0, column=7, padx=5, pady=5)
b20 = tk.Button(
    f1,
    text="20",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 20, 20),
)
b20.grid(row=1, column=7, padx=5, pady=5)
r19 = tk.Button(
    f1,
    text="19",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 19, 19),
)
r19.grid(row=2, column=7, padx=5, pady=5)
b24 = tk.Button(
    f1,
    text="24",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 24, 24),
)
b24.grid(row=0, column=8, padx=5, pady=5)
r23 = tk.Button(
    f1,
    text="23",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 23, 23),
)
r23.grid(row=1, column=8, padx=5, pady=5)
b22 = tk.Button(
    f1,
    text="22",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 22, 22),
)
b22.grid(row=2, column=8, padx=5, pady=5)
r27 = tk.Button(
    f1,
    text="27",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 27, 27),
)
r27.grid(row=0, column=9, padx=5, pady=5)
b26 = tk.Button(
    f1,
    text="26",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 26, 26),
)
b26.grid(row=1, column=9, padx=5, pady=5)
r25 = tk.Button(
    f1,
    text="25",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 25, 25),
)
r25.grid(row=2, column=9, padx=5, pady=5)
r30 = tk.Button(
    f1,
    text="30",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 30, 30),
)
r30.grid(row=0, column=10, padx=5, pady=5)
b29 = tk.Button(
    f1,
    text="29",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 29, 29),
)
b29.grid(row=1, column=10, padx=5, pady=5)
b28 = tk.Button(
    f1,
    text="28",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 28, 28),
)
b28.grid(row=2, column=10, padx=5, pady=5)
b33 = tk.Button(
    f1,
    text="33",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 33, 33),
)
b33.grid(row=0, column=11, padx=5, pady=5)
r32 = tk.Button(
    f1,
    text="32",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 32, 32),
)
r32.grid(row=1, column=11, padx=5, pady=5)
b31 = tk.Button(
    f1,
    text="31",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 31, 31),
)
b31.grid(row=2, column=11, padx=5, pady=5)
r36 = tk.Button(
    f1,
    text="36",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 36, 36),
)
r36.grid(row=0, column=12, padx=5, pady=5)
b35 = tk.Button(
    f1,
    text="35",
    bg="black",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 35, 35),
)
b35.grid(row=1, column=12, padx=5, pady=5)
r34 = tk.Button(
    f1,
    text="34",
    bg="red",
    fg="white",
    command=partial(payout, st.spinStraight, 35, 34, 34),
)
r34.grid(row=2, column=12, padx=5, pady=5)
# frame directly under 0-36 buttons (shortened to f2)
f2 = tk.Frame(root, bg="sea green", borderwidth=0)
f2.grid(row=1, column=0, sticky="ew")
# dozen buttons
g1st12 = tk.Button(
    f2,
    text="1st 12",
    bg="green",
    fg="white",
    width=16,
    command=partial(payout, st.spinStraight, 2, 1, 12),
)
g1st12.grid(row=0, column=1, padx=5, pady=5)
g2nd12 = tk.Button(
    f2,
    text="2nd 12",
    bg="green",
    fg="white",
    width=16,
    command=partial(payout, st.spinStraight, 2, 13, 24),
)
g2nd12.grid(row=0, column=2, padx=6, pady=5)
g3rd12 = tk.Button(
    f2,
    text="3rd 12",
    bg="green",
    fg="white",
    width=16,
    command=partial(payout, st.spinStraight, 2, 25, 36),
)
g3rd12.grid(row=0, column=3, padx=6, pady=5)
# frame below f2 (shortened to f3)
f3 = tk.Frame(root, bg="sea green", borderwidth=0)
f3.grid(row=2, column=0, sticky="ew")
# green buttons bottom row
g1to18 = tk.Button(
    f3,
    text="1 to 18",
    bg="green",
    fg="white",
    width=6,
    command=partial(payout, st.spinStraight, 1, 1, 18),
)
g1to18.grid(row=0, column=1, padx=5, pady=5)
gEVEN = tk.Button(
    f3,
    text="EVEN",
    bg="green",
    fg="white",
    width=6,
    command=partial(payout, st.spinRemainder, 1, 0, 2),
)
gEVEN.grid(row=0, column=2, padx=13, pady=5)
gRED = tk.Button(
    f3,
    text="◆",
    bg="green",
    fg="red",
    width=7,
    command=partial(payout, st.spinColor, 1, 0, 99),
)
gRED.grid(row=0, column=3, pady=5)
gBLACK = tk.Button(
    f3,
    text="◆",
    bg="green",
    fg="black",
    width=7,
    command=partial(payout, st.spinColor, 1, 99, 99),
)
gBLACK.grid(row=0, column=4, pady=5)
gODD = tk.Button(
    f3,
    text="ODD",
    bg="green",
    fg="white",
    width=6,
    command=partial(payout, st.spinRemainder, 1, 1, 2),
)
gODD.grid(row=0, column=5, padx=14, pady=5)
g19to36 = tk.Button(
    f3,
    text="19 to 36",
    bg="green",
    fg="white",
    width=6,
    command=partial(payout, st.spinStraight, 1, 19, 36),
)
g19to36.grid(row=0, column=6, padx=4, pady=5)
# frame below f3 (shortened to f4)
f4 = tk.Frame(root, bg="sea green")
f4.grid(row=3, column=0, sticky="ew")
# frame at the bottom (shortened to f5)
f5 = tk.Frame(root, bg="sea green", borderwidth=0)
f5.grid(row=4, column=0, sticky="ew")
# bet change buttons
c0 = tk.Button(f5, text="$1", bg="sea green", fg="black", command=partial(changeBet, 1))
c0.grid(row=0, column=0, padx=5, pady=5)
c1 = tk.Button(f5, text="$25", bg="white", fg="black", command=partial(changeBet, 25))
c1.grid(row=0, column=1, padx=5, pady=5)
c2 = tk.Button(f5, text="$100", bg="red", fg="white", command=partial(changeBet, 100))
c2.grid(row=0, column=2, padx=5, pady=5)
c3 = tk.Button(f5, text="$500", bg="green", fg="white", command=partial(changeBet, 500))
c3.grid(row=0, column=3, padx=5, pady=5)
c4 = tk.Button(
    f5, text="$1000", bg="black", fg="white", command=partial(changeBet, 1000)
)
c4.grid(row=0, column=4, padx=5, pady=5)
c5 = tk.Button(
    f5, text="$5000", bg="blue", fg="white", command=partial(changeBet, 5000)
)
c5.grid(row=0, column=5, padx=5, pady=5)
# disguised labels meant to offset buttons
f1offset1 = tk.Label(f1, text="", bg="sea green")
f1offset1.grid(row=0, column=0, pady=5)
f1offset2 = tk.Label(f1, text="", bg="sea green")
f1offset2.grid(row=2, column=0, pady=5)
f2offset = tk.Label(f2, text="", bg="sea green")
f2offset.grid(row=0, column=0, padx=14, pady=5)
f3offset = tk.Label(f3, text="", bg="sea green")
f3offset.grid(row=0, column=0, padx=14, pady=5)
# space between left and previous roll
spaceLabel1 = tk.Label(f4, textvariable="", bg="sea green", width=39)
spaceLabel1.grid(row=0, column=0, padx=2, pady=5)
# space between bet buttons and counters
spaceLabel2 = tk.Label(f5, textvariable="", bg="sea green")
spaceLabel2.grid(row=0, column=6, padx=9, pady=5)
# "dynamic" labels at the bottom
betDisplay = tk.StringVar(value="Bet: $" + str(bet.get()))
betLabel = tk.Label(
    f5, textvariable=betDisplay, font=("Times New Roman", 12), bg="white", width=9
)
betLabel.grid(row=0, column=7, pady=5)

chipsDisplay = tk.StringVar(value="Chips: $" + str(chips.get()))
chipsLabel = tk.Label(
    f5, textvariable=chipsDisplay, font=("Times New Roman", 12), bg="gray90", width=10
)
chipsLabel.grid(row=0, column=8, padx=5, pady=5)

spinDisplay = tk.StringVar(value="Roll: " + str(spinResult.get()))
lastSpinLabel = tk.Label(
    f4, textvariable=spinDisplay, font=("Times New Roman", 12), bg="ivory", width=9
)
lastSpinLabel.grid(row=0, column=1, padx=5, pady=5, sticky="sew")

payoutResultDisplay = tk.StringVar(value=str(payoutResult.get()))
payoutResultLabel = tk.Label(
    f4,
    textvariable=payoutResultDisplay,
    font=("Times New Roman", 12),
    bg="lime",
    width=10,
)
payoutResultLabel.grid(row=0, column=2, pady=5, sticky="sew")


root.mainloop()
