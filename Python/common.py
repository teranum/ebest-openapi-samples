from prettytable import *

# prettytable을 사용하여 데이터를 표로 이쁘게 출력하는 클래스
class print_table:
    def __init__(self, data):
        if isinstance(data, dict):
            table = PrettyTable(['key','value'])
            fields = data.items();
            table.add_rows([list(x) for x in fields])
            print(f"Field Count = {len(fields)}")
            print(table)
        elif isinstance(data, list):
            table = PrettyTable()
            table.field_names = data[0]
            table.add_rows([x.values() for x in data])
            print(f"Row Count = {len(data)}")
            print(table)
            
