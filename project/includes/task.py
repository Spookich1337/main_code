class Task:
    def __init__(self, name):
        self.name = name
        self.completed = False


    def change_status(self):
        if self.completed == True:
            self.completed = False
        else:
            self.completed = True

    
    def change_name(self, new_name):
        self.name = new_name


    def __str__(self):
        return f"{"Сделано" if self.completed == True else "Нужно сделать"}: {self.name}"

 
    def rename(self, new_name):
        self.name = new_name


class TaskList:
    def __init__(self, path = None):
        if path != None:
            self.__load_list(path)
        else:
            self.list = []
            

    def __load_list(self, path):
        pass


    def insert(self, new_task:str):
        self.list.append(Task(new_task))


    def delete(self, index:int):
        try:
            self.list.pop(index - 1)
            return True
        except IndexError:
            return False


    def new_name(self, index:int, new_name = None):
        try:
            self.list[index - 1].change_name(new_name)
            return True
        except  IndexError:
            return False


    
    def new_status(self, index:int):
        try:
            self.list[index - 1].change_status()
            return True
        except IndexError:
            return False

    
    def __str__(self):
        result = ""
        for i in range(len(self.list)):
            result += str(self.list[i])
            if (i != len(self.list) - 1):
                result += '\n'
        return result  