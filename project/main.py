from includes.task import TaskList
import os

"""инициализация общего листа"""
tasks = TaskList()

"""сет для определения хода"""
move_set = {"create": 1, "delete": 2, "rename": 3, "done": 4, "failed": 4, "exit": 5}


while True:
    tmp = list(map(str, input().split()))

    move = move_set.get(tmp[0], 786)

    match move:
        case 1:
            result = ""
            for i in range(1, len(tmp)):
                result += tmp[i] + " "
            tasks.insert(result)

        case 2:
            tasks.delete(int(tmp[1]))

        case 3:
            result = ""
            for i in range(2, len(tmp)):
                result += tmp[i] + " "
            tasks.new_name(int(tmp[1]), result)

        case 4: 
            tasks.new_status(int(tmp[1]))

        case 5:
            break

        case _:
            print("incorrect input")

    os.system("clear")
    print(tasks, '\n')