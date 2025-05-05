import src.includes as inc

while(True):
    print("Input type of solution(tsp/approx/exit)")
    user_input = input()

    if user_input == "tsp":
        print("Set size")
        n = int(input())
        graph = []
        print("Input matrix")
        for _ in range(n):
            row = list(map(int, input().split()))
            graph.append(row)

        cost, path = inc.tsp(graph, n)

        if cost == inc.INF:
            print("No path")
        else:
            print("Cost:")
            print(cost)
            print("Path:")
            print(' '.join(map(str, path)))
    elif user_input == "approx":
        print("Set size")
        n = int(input())
        print("Set start city(standart=0)")
        start = int(input())
        graph = []
        print("Input matrix")
        for _ in range(n):
            row = list(map(int, input().split()))
            graph.append(row)

        # Стартовый город фиксирован как 0
        path, cost = inc.approx(graph, start)

        if path == "no path":
            print("No path")
        else:
            print("Cost:")
            print(cost)
            print("Path:")
            print(' '.join(map(str, path)))
    elif user_input == "exit":
        break
    else:
        print("Inccorect input, pleas try again")