class FenwickTree():
    array = []
    tam = 0
    def __init__(self,arr):
        self.tam = len(arr) + 1
        self.array = [0]*(len(arr) + 1)
        for i in range(0,len(arr)):
            self.update(i,arr[i],len(arr))
    
    def sum(self,index):
        answer = 0
        index+=1
        while index > 0:
            answer += self.array[index]
            index -= index&(-index)
        return answer

    def update(self,index,value,size):
        index+=1
        while index <= size:
            self.array[index] += value
            index+= index&(-index)

