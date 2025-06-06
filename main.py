import argparse
import os


def report_payout(dct: dict[str, list[int | str]]):
    # разбить сотрудников по отделам
    deps: dict[str, list] = {}
    for idx, dep in enumerate(dct.get("department")):
        if not deps.get(dep):
            deps[dep] = []
        deps[dep].append([
            dct["name"][idx],
            dct["hours_worked"][idx],
            dct["hourly_rate"][idx],
            dct["hours_worked"][idx] * dct["hourly_rate"][idx],
        ])
    deps = dict(sorted(deps.items()))
    print("{:<15} {:10}\t{:10}{:10}{:10}".format("", "Name", "Hours", "Rate", "Payout") + "\n")
    for key, value in deps.items():
        print(key)
        for i in value:
            print("{:-^15} {:10}\t{:10}{:10}{:10}".format("", i[0], str(i[1]), str(i[2]), f'${i[3]}') + "\n")

        print("{:^15} {:10}\t{:10}{:10}{:10}".format("", "", str(sum([int(i[1]) for i in value])), "",
                                                     '$' + str(sum([int(i[3]) for i in value]))) + "\n")


def get_head_idx(head: list[str]) -> list[int]:
    idx = [
        head.index('id'),
        head.index('email'),
        head.index('name'),
        head.index('department'),
        head.index('hours_worked'),
    ]
    for i in ['hourly_rate', 'rate', 'salary']:
        if i in head:
            idx.append(head.index(i))
            break

    return idx


def main(files: list[str], report: str):
    if not files:
        print("Отсутствует список файлов")
        return
    dct: dict[str, list] = {
        "id": [],
        "email": [],
        "name": [],
        "department": [],
        "hours_worked": [],
        "hourly_rate": [],
    }
    # На вход поступают файлы, для каждого файла надо выделать соответствующие колонки
    for file in files:
        if not os.path.exists(file):
            print(file, 'не существует')
            continue
        with open(file, 'r') as f:
            data = f.readlines()
        id_idx, email_idx, name_idx, department_idx, hours_worked_idx, hourly_rate_idx = get_head_idx(
            data[0].strip().split(','))
        for row in data[1:]:
            values = row.strip().split(',')
            dct["id"].append(int(values[id_idx]))
            dct["email"].append(values[email_idx])
            dct["name"].append(values[name_idx])
            dct["department"].append(values[department_idx])
            dct["hours_worked"].append(int(values[hours_worked_idx]))
            dct["hourly_rate"].append(int(values[hourly_rate_idx]))
    match report:
        case 'payout':
            report_payout(dct)

        case _:
            print('Не существует отчета ', report)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Формирование отчетов по указанным файлам')

    parser.add_argument('files', nargs='*', help='Файлы для составления отчета')
    parser.add_argument('-r', '--report', help='Тип отчета')
    args = parser.parse_args()
    main(args.files, args.report)
