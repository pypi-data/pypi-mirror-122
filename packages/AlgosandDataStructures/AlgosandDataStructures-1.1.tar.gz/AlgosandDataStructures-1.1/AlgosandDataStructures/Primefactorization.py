import math

def Primefactorization(value):
    
    answer = []
    while value%2 == 0:
        answer.append(2)
        value = value / 2
    

    for i in range(3, math.floor(math.sqrt(value)) + 1,2):
        while int(value) % int(i) == 0:
            print(i)
            answer.append(int(i))
            value = value / i
    
    if value > 2:
        answer.append(int(value))
    
    return answer


print(Primefactorization(20))