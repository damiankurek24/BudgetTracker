from transaction_analyzer import TransactionAnalyzer

excel_file = 'C:/Users/Damian Kurek/PycharmProjects/TransactionAnalyzer/wyciag1.xls'
analyzer = TransactionAnalyzer(excel_file)

list_of_possible_operations = ['Lista możliwych operacji: \na) wyszukaj po typie transakcji',
                               '\nb) wyszukaj po odbiorcy', '\nc) podsumowanie transakcji',
                               '\nd)podsumowanie transakcji mieięcznie']

print(*list_of_possible_operations, sep=',')
choose_operation = input("Co zrobić z twoim wyciągiem?")

if choose_operation == 'a':
    analyzer.search_by_transaction_type()
elif choose_operation == 'b':
    analyzer.search_by_recipient()
elif choose_operation == 'c':
    analyzer.summarize_transactions()
elif choose_operation == 'd':
    analyzer.sumarize_transactions_monthly()

else:
    print("Wybrano nieprawidłową operację.")





