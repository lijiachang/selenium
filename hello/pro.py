def josephus(n,k):

    List = list(range(1,n+1))
    index = 0
    while List:
        print List
        temp = List.pop(0)
        index += 1
        if index == k:
            index = 0
            continue
        List.append(temp)
        if len(List)==1:
            print(List)
            break

if __name__ == '__main__':
    josephus(10,3)