import os
import csv
from itertools import islice

if __name__ == '__main__':
    data_path = '.\\testdata'
    filename = '\\transaction-report.csv'
    fee = amount = total_shares = 0.0
    exchange_and_symbol = dict()
    if os.path.isdir(data_path):
        try:
            with open(data_path + filename) as open_file:
                for row in islice(csv.reader(open_file), 1, None):
                    try:
                        if row[2] not in exchange_and_symbol[row[3]]:
                            exchange_and_symbol[row[3]].append(row[2])
                    except KeyError:
                        exchange_and_symbol[row[3]] = [row[2]]
            exchange = input("1. NASDAQ\n2. NYSE\n3. ASX\n4. NZX\n5. CBOE\nSelect:").strip()
            if exchange == '1':
                exchange = 'NASDAQ'
            elif exchange == '2':
                exchange = 'NYSE'
            elif exchange == '3':
                exchange = 'ASX'
            elif exchange == '4':
                exchange = 'NZX'
            elif exchange == '5':
                exchange = 'CBOE'
            for key in exchange_and_symbol.keys():
                exchange_and_symbol[key].sort()
            exchange_and_symbol_iter = exchange_and_symbol[exchange].__iter__()
            complete = False
            num, option_num = 1, 0
            while not complete:
                line_items = []
                for x in range(8):
                    try:
                        line_items.append(f'{num:<4}{exchange_and_symbol_iter.__next__():<8}')
                        num += 1
                    except StopIteration:
                        complete = True
                        break
                print("".join(line_items))
            while not 0 < option_num < num:
                try:
                    option = input('Select symbol:')
                    option_num = int(option.strip())
                    option_selected = option_num - 1
                except ValueError:
                    option = 0
            symbol = exchange_and_symbol[exchange][option_selected]
            with open(data_path + filename) as open_file:
                for row in csv.reader(open_file):
                    try:
                        if row[3] == exchange and row[2] == symbol:
                            total_shares += float(row[4])
                            fee += float(row[8])
                            amount += float(row[10])
                    except Exception as e:
                        print(e)
                        print(row)
                        break
            print(f'{symbol} {exchange}:')
            print(f'{total_shares=}, {fee=}, {amount=} Total spent: {fee + amount}')
        except FileNotFoundError:
            print(f"File {data_path + filename} not found")
    else:
        print(f'Folder {data_path} not found.')
