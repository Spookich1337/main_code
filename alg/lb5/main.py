import src.includes as lib

while(True):
    print("what do you want to use(aho/wild/exit)")
    user_input = input()

    if (user_input == "exit"):
        break

    if (user_input != "aho" and user_input != "wild"):
        print("incorrect input")
        continue

    print("do you wanna see how program work(1/0)")
    break_down_flag = int(input())

    if (user_input == "aho"):
        print("input text")
        text = input()

        print("input sub strings count")
        n = int(input())

        print("input sub strings")
        subs = []
        for i in range(n):
            subs.append(input())

        result = lib.aho_corasick_search(text, subs, break_down_flag)

        for pos,num in result:
            print(pos, num)

    elif (user_input =="wild"):
        print("input text")
        text = input()

        print("input sub string")
        sub = input()

        print("input wildcard char")
        wild_card = input()

        result = lib.wildcard_search(text, sub, wild_card,break_down_flag)

        for pos in result:
            print(pos)
