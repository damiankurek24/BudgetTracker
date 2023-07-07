import pandas as pd
import matplotlib as plt

class TransactionAnalyzer:
    def __init__(self, excel_file):
        self.df = pd.read_excel(excel_file, sheet_name=0,
                                usecols=['Data operacji', 'Typ transakcji', 'Kwota', 'Saldo po transakcji',
                                         'Nazwa odbiorcy', 'Rachunek odbiorcy', 'Nazwa nadawcy', 'Rachunek nadawcy',
                                         'Opis transakcji'])

    def getTransaction(self, thePaymentType, arguments):
        return self.df.loc[self.df['Typ transakcji'] == thePaymentType, arguments]

    def search_by_transaction_type(self):
        list_of_transactions = ['Wybierz spośród możliwych typów transakcji:\n'
                                'a) Płatność kartą', 'b) Przelew na rachunek', 'c) Przelew na telefon',
                                'd) Płatność web - kod mobilny',
                                'e) Zakup w terminalu - kod mobilny']
        print(*list_of_transactions, sep=',\n')
        wybierz_typ_transakcji = input("Wybierz typ transakcji: ")

        if wybierz_typ_transakcji == 'a':
            print(self.getTransaction("Płatność kartą", ['Data operacji', 'Kwota', 'Opis transakcji']))
        elif wybierz_typ_transakcji == 'b':
            print(self.getTransaction('Przelew na rachunek', ['Data operacji', 'Kwota', 'Rachunek nadawcy']))
        elif wybierz_typ_transakcji == 'c':
            print(self.df.loc[self.df['Typ transakcji'].isin(
                ["Przelew na telefon wychodzący zew.", "Przelew na telefon wychodzący wew.",
                 "Przelew na telefon przychodz. zew.", "Przelew na telefon przychodz. wew."]),
            ['Data operacji', 'Kwota', 'Nazwa odbiorcy']])
        elif wybierz_typ_transakcji == 'd':
            print(self.getTransaction('Płatność web - kod mobilny', ['Data operacji', 'Kwota', 'Opis transakcji']))
        elif wybierz_typ_transakcji == 'Zakup w terminalu - kod mobilny':
            print(self.getTransaction('Zakup w terminalu - kod mobilny', ['Data operacji', 'Kwota', 'Opis transakcji']))
        else:
            print("Wybrano nieprawidłowy typ transakcji.")

    def search_by_recipient(self):
        nazwa_odbiorcy = input("Wpisz nazwe odbiorcy")
        self.df['Nazwa odbiorcy'].fillna('', inplace=True)  # fill missing values with empty string
        found = self.df.loc[
            self.df['Nazwa odbiorcy'].str.contains(nazwa_odbiorcy, case=False), ['Data operacji', 'Kwota',
                                                                                 'Nazwa odbiorcy']]
        print(found)

    def summarize_transactions(self):
        column_sum = self.df['Kwota'].sum()
        column_min = self.df['Kwota'].min()
        column_max = self.df['Kwota'].max()
        column_summary = self.df['Kwota'].describe().round(2)

        print("Suma:", format(column_sum, '.2f'))
        print("Minimum:", format(column_min, '.2f'))
        print("Maximum:", format(column_max, '.2f'))

    def sumarize_transactions_monthly(self):
        choose_month = int(input("Wybierz miesiąc dla którego chcesz podsumować transakcję: 0-12: "))
        self.df['Data operacji'] = pd.to_datetime(self.df['Data operacji'])
        first_day = pd.to_datetime(f"{self.df['Data operacji'].dt.year[0]}-{choose_month:02d}-01")
        last_day = first_day + pd.offsets.MonthEnd()
        wynik = self.df[(self.df['Data operacji'] >= first_day) & (self.df['Data operacji'] <= last_day)]
        wybrane_kolumny = ['Saldo po transakcji', 'Data operacji', 'Kwota']
        wynik = wynik.loc[:, wybrane_kolumny]

        wynik = wynik.sort_values('Data operacji')

        daty = wynik['Data operacji'].dt.day
        saldo = wynik['Saldo po transakcji']
        kwota_transakcji = wynik['Kwota']

        plt.plot(daty, saldo, marker='o', linestyle='-')
        # Dodanie etykiet osi
        plt.xlabel('Dzień')
        plt.ylabel('Saldo po transakcji')

        # Dodanie tytułu wykresu
        plt.title('Zmiana salda po transakcji w ciągu miesiąca')

        plt.grid(True)
        plt.show()