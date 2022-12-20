list1 = [1, 2, 3, 4, 5, 2, 2]
for i in list1:
    if i == 2:
        list1.remove(i)
print(list1)


# list1 = [1, 2, 3, 4, 5, 2, 2]
# for i in range(len(list1)):
#     if list1[i] == 2:
#         list1.remove(list1[i])
          # IndexError: list index out of range
# print(list1)

list1 = [1, 2, 3, 4, 5, 2, 2]
list2 = list(filter(lambda x: x!=2, list1))
print(list2)

list1 = [1, 2, 3, 4, 5, 2, 2]
list2 = [i for i in list1 if i!=2]
print(list2)

list1 = [1, 2, 3, 4, 5, 2, 2]
for i in list1[:]:
    if i == 2:
        list1.remove(i)
print(list1)

import copy

list1 = [1, 2, 3, 4, 5, 2, 2]
# list2 = copy.copy(list1)
list2 = copy.deepcopy(list1)
for i in list1:
    if i == 2:
        list2.remove(i)
print(list2)

list1 = [1, 2, 3, 4, 5, 2, 2]
while 2 in list1:
    list1.remove(2)
print(list1)
