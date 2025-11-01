#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplikacja do interpolacji temperatury na długości czujnika światłowodowego
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class InterpolacjaTemperatury:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpolacja Temperatury - Czujnik Światłowodowy")
        self.root.geometry("1200x800")

        # Dane czujników
        self.czujniki = []  # Lista tupli: (nazwa, pozycja, temperatura)

        # Utworzenie interfejsu
        self.utworz_interfejs()

    def utworz_interfejs(self):
        # Główny kontener z dwoma kolumnami
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Lewa kolumna - panel sterowania
        left_frame = ttk.LabelFrame(main_frame, text="Panel Sterowania", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Prawa kolumna - wyniki
        right_frame = ttk.LabelFrame(main_frame, text="Wyniki", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)

        # Konfiguracja responsywności
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # === LEWA KOLUMNA ===

        # Sekcja 1: Parametry światłowodu
        param_frame = ttk.LabelFrame(left_frame, text="Parametry Światłowodu", padding="10")
        param_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(param_frame, text="Długość światłowodu [m]:").grid(row=0, column=0, sticky=tk.W)
        self.dlugosc_var = tk.StringVar(value="100")
        ttk.Entry(param_frame, textvariable=self.dlugosc_var, width=15).grid(row=0, column=1, padx=5)

        ttk.Label(param_frame, text="Rozdzielczość [m]:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.rozdzielczosc_var = tk.StringVar(value="0.5")
        ttk.Entry(param_frame, textvariable=self.rozdzielczosc_var, width=15).grid(row=1, column=1, padx=5)

        ttk.Label(param_frame, text="Stopień wielomianu:").grid(row=2, column=0, sticky=tk.W)
        self.stopien_var = tk.StringVar(value="3")
        ttk.Entry(param_frame, textvariable=self.stopien_var, width=15).grid(row=2, column=1, padx=5)

        # Separator
        ttk.Separator(param_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Opcje skali osi Y
        ttk.Label(param_frame, text="Skala osi Y:").grid(row=4, column=0, sticky=tk.W)
        self.auto_scale_y = tk.BooleanVar(value=True)
        ttk.Checkbutton(param_frame, text="Automatyczna", variable=self.auto_scale_y,
                       command=self.toggle_y_scale).grid(row=4, column=1, sticky=tk.W, padx=5)

        ttk.Label(param_frame, text="Y min [°C]:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.y_min_var = tk.StringVar(value="0")
        self.y_min_entry = ttk.Entry(param_frame, textvariable=self.y_min_var, width=15, state='disabled')
        self.y_min_entry.grid(row=5, column=1, padx=5)

        ttk.Label(param_frame, text="Y max [°C]:").grid(row=6, column=0, sticky=tk.W)
        self.y_max_var = tk.StringVar(value="50")
        self.y_max_entry = ttk.Entry(param_frame, textvariable=self.y_max_var, width=15, state='disabled')
        self.y_max_entry.grid(row=6, column=1, padx=5)

        # Separator
        ttk.Separator(param_frame, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        # Opcje ekstrapolacji
        ttk.Label(param_frame, text="Ekstrapolacja:").grid(row=8, column=0, sticky=tk.W)
        self.wirtualne_czujniki = tk.BooleanVar(value=True)
        ttk.Checkbutton(param_frame, text="Wirtualne czujniki", variable=self.wirtualne_czujniki).grid(row=8, column=1, sticky=tk.W, padx=5)

        # Tooltip/opis
        info_label = ttk.Label(param_frame, text="(płaska ekstrapolacja na skrajach)", font=('TkDefaultFont', 8), foreground='gray')
        info_label.grid(row=9, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))

        # Sekcja 2: Dodawanie czujników
        czujnik_frame = ttk.LabelFrame(left_frame, text="Dodaj Czujnik", padding="10")
        czujnik_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(czujnik_frame, text="Nazwa czujnika:").grid(row=0, column=0, sticky=tk.W)
        self.nazwa_var = tk.StringVar()
        ttk.Entry(czujnik_frame, textvariable=self.nazwa_var, width=15).grid(row=0, column=1, padx=5)

        ttk.Label(czujnik_frame, text="Pozycja [m]:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.pozycja_var = tk.StringVar()
        ttk.Entry(czujnik_frame, textvariable=self.pozycja_var, width=15).grid(row=1, column=1, padx=5)

        ttk.Label(czujnik_frame, text="Temperatura [°C]:").grid(row=2, column=0, sticky=tk.W)
        self.temperatura_var = tk.StringVar()
        ttk.Entry(czujnik_frame, textvariable=self.temperatura_var, width=15).grid(row=2, column=1, padx=5)

        ttk.Button(czujnik_frame, text="Dodaj Czujnik",
                  command=self.dodaj_czujnik).grid(row=3, column=0, columnspan=2, pady=10)

        # Sekcja 3: Lista czujników
        lista_frame = ttk.LabelFrame(left_frame, text="Lista Czujników", padding="10")
        lista_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        left_frame.rowconfigure(2, weight=1)

        # Treeview do wyświetlania czujników
        columns = ("Nazwa", "Pozycja [m]", "Temperatura [°C]")
        self.czujniki_tree = ttk.Treeview(lista_frame, columns=columns, show="headings", height=8)

        for col in columns:
            self.czujniki_tree.heading(col, text=col)
            self.czujniki_tree.column(col, width=100)

        self.czujniki_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbar dla listy
        scrollbar = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.czujniki_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.czujniki_tree.configure(yscrollcommand=scrollbar.set)

        ttk.Button(lista_frame, text="Usuń Zaznaczony",
                  command=self.usun_czujnik).grid(row=1, column=0, pady=5)

        # Sekcja 4: Akcje
        akcje_frame = ttk.Frame(left_frame)
        akcje_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)

        ttk.Button(akcje_frame, text="Oblicz Interpolację",
                  command=self.oblicz_interpolacje,
                  style="Accent.TButton").grid(row=0, column=0, padx=5, sticky=(tk.W, tk.E))

        ttk.Button(akcje_frame, text="Wyczyść Wszystko",
                  command=self.wyczysc_wszystko).grid(row=0, column=1, padx=5, sticky=(tk.W, tk.E))

        akcje_frame.columnconfigure(0, weight=1)
        akcje_frame.columnconfigure(1, weight=1)

        # === PRAWA KOLUMNA ===

        # Sekcja: Wzór wielomianu
        wzor_frame = ttk.LabelFrame(right_frame, text="Wzór Wielomianu Interpolacyjnego", padding="10")
        wzor_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        self.wzor_text = scrolledtext.ScrolledText(wzor_frame, height=6, width=60, wrap=tk.WORD)
        self.wzor_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        wzor_frame.columnconfigure(0, weight=1)

        # Sekcja: Wykres
        wykres_frame = ttk.LabelFrame(right_frame, text="Wykres Interpolacji", padding="10")
        wykres_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        right_frame.rowconfigure(1, weight=1)

        # Utworzenie figury matplotlib
        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=wykres_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        wykres_frame.rowconfigure(0, weight=1)
        wykres_frame.columnconfigure(0, weight=1)

        # Inicjalizacja pustego wykresu
        self.ax.set_xlabel("Pozycja na światłowodzie [m]")
        self.ax.set_ylabel("Temperatura [°C]")
        self.ax.set_title("Rozkład temperatury")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()

    def toggle_y_scale(self):
        """Włącza/wyłącza ręczne ustawienie skali osi Y"""
        if self.auto_scale_y.get():
            self.y_min_entry.config(state='disabled')
            self.y_max_entry.config(state='disabled')
        else:
            self.y_min_entry.config(state='normal')
            self.y_max_entry.config(state='normal')

    def dodaj_czujnik(self):
        """Dodaje nowy czujnik do listy"""
        try:
            nazwa = self.nazwa_var.get().strip()
            pozycja = float(self.pozycja_var.get())
            temperatura = float(self.temperatura_var.get())

            if not nazwa:
                messagebox.showwarning("Ostrzeżenie", "Nazwa czujnika nie może być pusta!")
                return

            # Sprawdzenie czy pozycja nie przekracza długości światłowodu
            dlugosc = float(self.dlugosc_var.get())
            if pozycja < 0 or pozycja > dlugosc:
                messagebox.showwarning("Ostrzeżenie",
                                      f"Pozycja musi być w zakresie 0-{dlugosc} m!")
                return

            # Dodanie czujnika
            self.czujniki.append((nazwa, pozycja, temperatura))

            # Aktualizacja widoku
            self.czujniki_tree.insert("", tk.END, values=(nazwa, pozycja, temperatura))

            # Wyczyszczenie pól
            self.nazwa_var.set("")
            self.pozycja_var.set("")
            self.temperatura_var.set("")

        except ValueError:
            messagebox.showerror("Błąd", "Pozycja i temperatura muszą być liczbami!")

    def usun_czujnik(self):
        """Usuwa zaznaczony czujnik"""
        selected = self.czujniki_tree.selection()
        if not selected:
            messagebox.showwarning("Ostrzeżenie", "Nie zaznaczono czujnika!")
            return

        # Pobranie indeksu
        index = self.czujniki_tree.index(selected[0])

        # Usunięcie z listy i widoku
        del self.czujniki[index]
        self.czujniki_tree.delete(selected[0])

    def wyczysc_wszystko(self):
        """Czyści wszystkie dane"""
        self.czujniki.clear()
        for item in self.czujniki_tree.get_children():
            self.czujniki_tree.delete(item)

        self.wzor_text.delete(1.0, tk.END)

        # Wyczyszczenie wykresu
        self.ax.clear()
        self.ax.set_xlabel("Pozycja na światłowodzie [m]")
        self.ax.set_ylabel("Temperatura [°C]")
        self.ax.set_title("Rozkład temperatury")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()

    def oblicz_interpolacje(self):
        """Oblicza interpolację wielomianową i wyświetla wyniki"""
        if len(self.czujniki) < 2:
            messagebox.showwarning("Ostrzeżenie",
                                  "Potrzeba co najmniej 2 czujników do interpolacji!")
            return

        try:
            # Pobranie parametrów
            dlugosc = float(self.dlugosc_var.get())
            rozdzielczosc = float(self.rozdzielczosc_var.get())
            stopien = int(self.stopien_var.get())

            # Walidacja stopnia wielomianu (ostrzeżenie, ale nie blokada)
            if stopien < 1:
                messagebox.showerror("Błąd", "Stopień wielomianu musi być co najmniej 1!")
                return

            if stopien > 10:
                odpowiedz = messagebox.askyesno("Ostrzeżenie",
                    f"Stopień wielomianu ({stopien}) jest bardzo wysoki.\n"
                    f"To może prowadzić do niestabilności numerycznej i oscylacji.\n"
                    f"Czy na pewno chcesz kontynuować?")
                if not odpowiedz:
                    return

            # Sortowanie czujników według pozycji
            czujniki_sorted = sorted(self.czujniki, key=lambda x: x[1])

            # Przygotowanie danych do interpolacji
            pozycje = np.array([c[1] for c in czujniki_sorted])
            temperatury = np.array([c[2] for c in czujniki_sorted])

            # Określenie zakresów rzeczywistych czujników (przed dodaniem wirtualnych)
            min_czujnik = pozycje.min()
            max_czujnik = pozycje.max()

            # Temperatury skrajnych czujników (dla wirtualnych czujników)
            temp_pierwszego = temperatury[0]  # Temperatura pierwszego czujnika
            temp_ostatniego = temperatury[-1]  # Temperatura ostatniego czujnika

            # Lista wirtualnych czujników do wizualizacji
            wirtualne_punkty = []

            # Dodanie wirtualnych czujników dla stabilnej ekstrapolacji
            if self.wirtualne_czujniki.get():
                # Wirtualne czujniki przed pierwszym czujnikiem (wszystkie z tą samą temp.)
                # Dodajemy 3 wirtualne czujniki dla lepszej stabilizacji
                if min_czujnik > 0:
                    for i in range(3, 0, -1):
                        pozycje = np.insert(pozycje, 0, min_czujnik - i)
                        temperatury = np.insert(temperatury, 0, temp_pierwszego)
                    # Zapisz tylko pierwszy do wizualizacji
                    wirtualne_punkty.append((min_czujnik - 3, temp_pierwszego))

                # Wirtualne czujniki za ostatnim czujnikiem (wszystkie z tą samą temp.)
                # Dodajemy 3 wirtualne czujniki dla lepszej stabilizacji
                if max_czujnik < dlugosc:
                    for i in range(1, 4):
                        pozycje = np.append(pozycje, max_czujnik + i)
                        temperatury = np.append(temperatury, temp_ostatniego)
                    # Zapisz tylko pierwszy do wizualizacji
                    wirtualne_punkty.append((max_czujnik + 1, temp_ostatniego))

            # Interpolacja wielomianowa (z wirtualnymi czujnikami jeśli włączone)
            wspolczynniki = np.polyfit(pozycje, temperatury, stopien)
            wielomian = np.poly1d(wspolczynniki)

            # Generowanie wzoru wielomianu
            wzor = self.generuj_wzor_wielomianu(wspolczynniki, min_czujnik, max_czujnik, dlugosc,
                                                 wirtualne_punkty, temp_pierwszego, temp_ostatniego)

            # Wyświetlenie wzoru
            self.wzor_text.delete(1.0, tk.END)
            self.wzor_text.insert(1.0, wzor)

            # Generowanie punktów do wykresu
            x_interpol = np.arange(0, dlugosc + rozdzielczosc, rozdzielczosc)
            y_interpol = wielomian(x_interpol)

            # Rysowanie wykresu
            self.ax.clear()

            # Oznaczenie obszarów ekstrapolacji (zacieniowanie)
            y_min, y_max = self.ax.get_ylim()
            if y_min == 0 and y_max == 1:  # Domyślne wartości, trzeba je ustawić
                y_min = min(temperatury.min(), y_interpol.min()) - 5
                y_max = max(temperatury.max(), y_interpol.max()) + 5

            # Ekstrapolacja przed pierwszym czujnikiem
            if min_czujnik > 0:
                self.ax.axvspan(0, min_czujnik, alpha=0.15, color='orange',
                               label='Ekstrapolacja')

            # Ekstrapolacja po ostatnim czujniku
            if max_czujnik < dlugosc:
                self.ax.axvspan(max_czujnik, dlugosc, alpha=0.15, color='orange')

            # Krzywa interpolacji/ekstrapolacji
            # Podziel na segmenty dla różnych kolorów
            mask_interpol = (x_interpol >= min_czujnik) & (x_interpol <= max_czujnik)
            mask_ekstra_left = x_interpol < min_czujnik
            mask_ekstra_right = x_interpol > max_czujnik

            # Rysowanie krzywej w obszarze interpolacji (niebieski, ciągły)
            if np.any(mask_interpol):
                self.ax.plot(x_interpol[mask_interpol], y_interpol[mask_interpol],
                           'b-', linewidth=2, label='Interpolacja')

            # Rysowanie krzywej w obszarach ekstrapolacji (niebieski, przerywany)
            if np.any(mask_ekstra_left):
                self.ax.plot(x_interpol[mask_ekstra_left], y_interpol[mask_ekstra_left],
                           'b--', linewidth=2, alpha=0.7)
            if np.any(mask_ekstra_right):
                self.ax.plot(x_interpol[mask_ekstra_right], y_interpol[mask_ekstra_right],
                           'b--', linewidth=2, alpha=0.7)

            # Punkty pomiarowe (rzeczywiste czujniki)
            rzeczywiste_poz = np.array([c[1] for c in czujniki_sorted])
            rzeczywiste_temp = np.array([c[2] for c in czujniki_sorted])
            self.ax.plot(rzeczywiste_poz, rzeczywiste_temp, 'ro', markersize=8,
                        label='Pomiary czujników', zorder=5)

            # Dodanie etykiet do punktów pomiarowych
            for nazwa, poz, temp in czujniki_sorted:
                self.ax.annotate(nazwa, (poz, temp),
                               xytext=(5, 5), textcoords='offset points',
                               fontsize=8, alpha=0.7)

            # Wirtualne czujniki (jeśli używane)
            if wirtualne_punkty:
                wirt_poz = [p[0] for p in wirtualne_punkty]
                wirt_temp = [p[1] for p in wirtualne_punkty]
                self.ax.plot(wirt_poz, wirt_temp, 'gs', markersize=8,
                           label='Wirtualne czujniki', zorder=4, alpha=0.7)

                # Etykiety dla wirtualnych czujników
                for i, (poz, temp) in enumerate(wirtualne_punkty):
                    if poz < 0:
                        label_text = "Wirt. (lewy)"
                    else:
                        label_text = "Wirt. (prawy)"
                    self.ax.annotate(label_text, (poz, temp),
                                   xytext=(5, 5), textcoords='offset points',
                                   fontsize=7, alpha=0.6, color='green')

            # Pionowe linie na pozycjach skrajnych czujników
            self.ax.axvline(min_czujnik, color='gray', linestyle=':', alpha=0.5, linewidth=1)
            self.ax.axvline(max_czujnik, color='gray', linestyle=':', alpha=0.5, linewidth=1)

            self.ax.set_xlabel("Pozycja na światłowodzie [m]", fontsize=10)
            self.ax.set_ylabel("Temperatura [°C]", fontsize=10)

            # Tytuł z informacją o zakresie
            title = f"Rozkład temperatury - wielomian stopnia {stopien}\n"
            title += f"(zakres czujników: {min_czujnik:.1f} - {max_czujnik:.1f} m)"
            self.ax.set_title(title, fontsize=11)

            self.ax.legend(loc='best')
            self.ax.grid(True, alpha=0.3)
            self.ax.set_xlim(-1, dlugosc + 1)

            # Ustawienie skali osi Y
            if not self.auto_scale_y.get():
                try:
                    y_min = float(self.y_min_var.get())
                    y_max = float(self.y_max_var.get())
                    if y_min >= y_max:
                        messagebox.showwarning("Ostrzeżenie",
                            "Y min musi być mniejsze niż Y max! Używam skali automatycznej.")
                    else:
                        self.ax.set_ylim(y_min, y_max)
                except ValueError:
                    messagebox.showwarning("Ostrzeżenie",
                        "Nieprawidłowe wartości skali Y! Używam skali automatycznej.")

            self.canvas.draw()

            # Informacja o sukcesie
            messagebox.showinfo("Sukces", "Interpolacja została obliczona pomyślnie!")

        except ValueError as e:
            messagebox.showerror("Błąd", f"Błąd w parametrach: {str(e)}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")

    def generuj_wzor_wielomianu(self, wspolczynniki, min_czujnik, max_czujnik, dlugosc,
                                 wirtualne_punkty=None, temp_pierwszego=None, temp_ostatniego=None):
        """Generuje tekstowy wzór wielomianu"""
        stopien = len(wspolczynniki) - 1
        wzor_parts = ["T(x) = "]

        for i, wsp in enumerate(wspolczynniki):
            wykladnik = stopien - i

            # Formatowanie współczynnika
            if abs(wsp) < 1e-10:  # Pomijanie bardzo małych współczynników
                continue

            # Znak
            if i > 0:
                znak = " + " if wsp >= 0 else " - "
            else:
                znak = "" if wsp >= 0 else "-"

            # Wartość bezwzględna współczynnika
            wsp_abs = abs(wsp)

            # Formatowanie współczynnika (naukowe dla bardzo małych/dużych liczb)
            if wsp_abs < 0.001 or wsp_abs > 1000:
                wsp_str = f"{wsp_abs:.4e}"
            else:
                wsp_str = f"{wsp_abs:.6f}".rstrip('0').rstrip('.')

            # Składanie członu
            if wykladnik == 0:
                czlon = f"{znak}{wsp_str}"
            elif wykladnik == 1:
                if wsp_abs == 1.0:
                    czlon = f"{znak}x"
                else:
                    czlon = f"{znak}{wsp_str}·x"
            else:
                if wsp_abs == 1.0:
                    czlon = f"{znak}x^{wykladnik}"
                else:
                    czlon = f"{znak}{wsp_str}·x^{wykladnik}"

            wzor_parts.append(czlon)

        wzor = "".join(wzor_parts)

        # Dodanie informacji o współczynnikach
        wzor += "\n\nWspółczynniki (od najwyższego stopnia):\n"
        for i, wsp in enumerate(wspolczynniki):
            wykladnik = stopien - i
            wzor += f"  a_{wykladnik} = {wsp:.10f}\n"

        # Dodanie informacji o dokładności
        wzor += f"\nStopień wielomianu: {stopien}\n"

        # Informacje o zakresach
        wzor += "\n" + "="*50 + "\n"
        wzor += "ZAKRESY:\n"
        wzor += f"Długość światłowodu: 0 - {dlugosc} m\n"
        wzor += f"Zakres czujników: {min_czujnik} - {max_czujnik} m\n"

        # Obszary ekstrapolacji
        if min_czujnik > 0:
            wzor += f"Ekstrapolacja LEWA: 0 - {min_czujnik} m\n"
        if max_czujnik < dlugosc:
            wzor += f"Ekstrapolacja PRAWA: {max_czujnik} - {dlugosc} m\n"

        wzor += f"\nInterpolacja: {min_czujnik} - {max_czujnik} m\n"

        # Informacje o wirtualnych czujnikach
        if wirtualne_punkty:
            wzor += "\n" + "="*50 + "\n"
            wzor += "WIRTUALNE CZUJNIKI:\n"
            wzor += f"Temperatura pierwszego czujnika: {temp_pierwszego:.2f} °C\n"
            wzor += f"Temperatura ostatniego czujnika: {temp_ostatniego:.2f} °C\n"
            wzor += "\nPozycje wirtualnych czujników:\n"
            for poz, temp in wirtualne_punkty:
                if poz < min_czujnik:
                    wzor += f"  • Lewe (pozycje {poz:.0f}, {poz+1:.0f}, {poz+2:.0f} m): {temp:.2f} °C\n"
                else:
                    wzor += f"  • Prawe (pozycje {poz:.0f}, {poz+1:.0f}, {poz+2:.0f} m): {temp:.2f} °C\n"
            wzor += "\nℹ Po 3 wirtualne czujniki na każdym końcu zapewniają\n"
            wzor += "  stabilną, płaską ekstrapolację bez oscylacji."

        # Ostrzeżenie o ekstrapolacji
        if min_czujnik > 0 or max_czujnik < dlugosc:
            wzor += "\n\n⚠ UWAGA: Wyniki w obszarach ekstrapolacji mogą być\n"
            wzor += "  mniej dokładne niż w obszarze między czujnikami!"

        return wzor


def main():
    root = tk.Tk()
    app = InterpolacjaTemperatury(root)
    root.mainloop()


if __name__ == "__main__":
    main()
