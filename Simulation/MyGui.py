import tkinter as tk


class MyGui:
    def __init__(self, size: int, length: int):
        self.root = tk.Tk()
        self.root.title("Symulacja kas w sklepie")

        # Kwadraty czerwone - kasy
        self.squares_big = []
        for i in range(size):
            square = tk.Canvas(self.root, width=40, height=40, bg="red", highlightthickness=0)
            square.grid(row=0, column=i, padx=2, pady=2)
            self.squares_big.append(square)

        # Kwadraty białe z ramką czarną - klienci
        self.squares_small = []
        for i in range(length):
            row_squares = []
            for j in range(size):
                square = tk.Canvas(self.root, width=30, height=30, bg="white", highlightthickness=1,
                                   highlightbackground="black")
                square.grid(row=i + 1, column=j, padx=2, pady=2)
                row_squares.append(square)
            self.squares_small.append(row_squares)

        self.status_legend = tk.Label(self.root, text="Legenda kolory kas: ", fg="black")
        self.status_legend.grid(row=4, column=size)

        self.status_active = tk.Label(self.root, text="aktywna", fg="green")
        self.status_active.grid(row=5, column=size)

        self.status_closed = tk.Label(self.root, text="zamknięta", fg="red")
        self.status_closed.grid(row=6, column=size)

        self.status_problem = tk.Label(self.root, text="problem z klientem", fg="orange")
        self.status_problem.grid(row=7, column=size)

        self.status_repair = tk.Label(self.root, text="w naprawie", fg="gray")
        self.status_repair.grid(row=8, column=size)

        self.time_label = tk.Label(self.root, text="Godzina 8:00", fg="black")
        self.time_label.grid(row=1, column=size)

        self.day_label = tk.Label(self.root, text="Poniedzialek", fg="black")
        self.day_label.grid(row=0, column=size)

    def klient_change_color(self, row, column, color):
        self.squares_small[row][column].configure(bg=color)
        self.root.update()

    def klienci_change_color(self, column, numberOfClients, length: 1):
        for i in range(length):
            self.klient_change_color(i, column, "white")

        for i in range(numberOfClients):
            self.klient_change_color(i, column, "black")
        self.root.update()

    def kasa_change_color(self, col, color):
        self.squares_big[col].configure(bg=color)
        self.root.update()

    def display_numbers(self, num1, num2):
        self.time_label.configure(text=f"Godzina: {num1}:{num2}")
        self.root.update()

    def display_days(self, num1):
        if(num1 == 0):
            self.day_label.configure(text=f"Poniedzialek")
        if (num1 == 1):
            self.day_label.configure(text=f"Wtorek")
        if (num1 == 2):
            self.day_label.configure(text=f"Sroda")
        if (num1 == 3):
            self.day_label.configure(text=f"Czwartek")
        if (num1 == 4):
            self.day_label.configure(text=f"Piatek")
        if (num1 == 5):
            self.day_label.configure(text=f"Sobota")
        if (num1 == 6):
            self.day_label.configure(text=f"Niedziela")
        self.root.update()
    def run(self):
        self.root.mainloop()