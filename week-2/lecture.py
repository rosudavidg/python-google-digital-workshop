print('Acesta este cursul al doilea')

name = 'Ana'

if name:
    print(name)
else:
    print("Nu avem definit niciun nume")

first_person = {'Name': 'John'}
second_person = {'Name': 'John'}

if first_person is second_person:
    print("They are the same")
else:
    print("They are not the same")

if first_person == second_person:
    print("They are the same")
else:
    print("They are not the same")

print('Hel\
lo')

print('''Ce faci?
Bine?''')


def func():
    '''Clasa asta nu face nimic'''
    pass


print(r'David\n\nare mere')
print('David\n\nare mere')

s = r'David\n\nare mere'
print(s)

# print(f'ceva {vc         }')

l = ['da', 'nu', 'ce']
for index, value in enumerate(l):
    print(f'{value} se afla la pozitia {index}')

A = {100, 7, 8}
B = {200, 4, 5}
C = {300, 2, 3, 7}
D = {100, 200, 300}

print(A & C)
print(A & D)
