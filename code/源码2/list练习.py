list1=[1,4,5,2,3,8,9,10,6,7]
print(list1)
s=0
for i in list1:
    s+=i
print(s)
print(sum(list1))
print(max(list1))
print(min(list1))
list1.sort(reverse=True)
print(list1)
list1.sort()
print(list1)
list1.reverse()
print(list1)