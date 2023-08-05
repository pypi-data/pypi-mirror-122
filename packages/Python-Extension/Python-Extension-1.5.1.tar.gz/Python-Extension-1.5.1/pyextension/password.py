# -*- coding:utf-8  -*-

dic = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-=_+|;:\'\",./?<>[]{} \n'

class Encrypt():
    def __init__(self, original, undo=True):
        self.original = original
        self.ciphertext = original
        self.isundo = undo
        if self.isundo == True:
            self.done = [self.original]
    def get(self):
        return self.ciphertext
    def undo(self):
        if self.isundo == True:
            try:
                self.ciphertext = self.done[-2]
                del self.done[-2]
                if self.isundo == True:
                    self.done.append(self.ciphertext)
            except IndexError:
                pass
    def reset(self):
        self.ciphertext = self.original
        if self.isundo == True:
            self.done.append(self.ciphertext)
    def set(self, value):
        self.ciphertext = value
        if self.isundo == True:
            self.done.append(self.ciphertext)
    def reverse(self):
        self.ciphertext = self.ciphertext[::-1]
        if self.isundo == True:
            self.done.append(self.ciphertext)
    def caesar_cipher(self, key, dic=dic):
        result = ''
        for x in self.ciphertext:
            index = dic.find(x)
            if index == -1:
                result += x
            else:
                index += key
                index %= len(dic)
                result += dic[index]
        self.ciphertext = result
        if self.isundo == True:
            self.done.append(self.ciphertext)
    def caesar(self, key, dic=dic) -> 'Caesar Cipher':
        self.caesar_cipher(key, dic)
    def vigenere_cipher(self, key, dic=dic):
        result = ''
        keys = []
        for x in key:
            if dic.find(x) != -1:
                keys.append(dic.find(x))
            else:
                raise KeyError('Key \'%s\' not found' % x)
        key_index = 0
        for x in self.ciphertext:
            index = dic.find(x)
            if index == -1:
                result += x
            else:
                index += keys[key_index]
                index %= len(dic)
                result += dic[index]
            key_index += 1
            key_index %= len(keys)
        self.ciphertext = result
        if self.isundo == True:
            self.done.append(self.ciphertext)
    def vigenere(self, key, dic=dic) -> 'Vigenere Cipher encrypt':
        self.vigenere_cipher(key, dic)
    def method(self, key, dic=dic):
        pass

class Decrypt():
    def __init__(self, ciphertext, undo=True):
        self.ciphertext = ciphertext
        self.original = ciphertext
        self.isundo = undo
        if self.isundo == True:
            self.done = [self.ciphertext]
    def get(self):
        return self.original
    def undo(self):
        if self.isundo == True:
            try:
                self.original = self.done[-2]
                del self.done[-2]
                if self.isundo == True:
                    self.done.append(self.original)
            except IndexError:
                pass
    def reset(self):
        self.original = self.ciphertext
        if self.isundo == True:
            self.done.append(self.original)
    def set(self, value):
        self.original = value
        if self.isundo == True:
            self.done.append(self.original)
    def reverse(self):
        self.original = self.original[::-1]
        if self.isundo == True:
            self.done.append(self.original)
    def caesar_cipher(self, key, dic=dic):
        result = ''
        for x in self.original:
            index = dic.find(x)
            if index == -1:
                result += x
            else:
                index -= key
                index %= len(dic)
                result += dic[index]
        self.original = result
        if self.isundo == True:
            self.done.append(self.original)
    def caesar(self, key, dic=dic) -> 'Caesar Cipher decrypt':
        self.caesar_cipher(key, dic)
    def vigenere_cipher(self, key, dic=dic):
        result = ''
        keys = []
        for x in key:
            if dic.find(x) != -1:
                keys.append(dic.find(x))
            else:
                raise KeyError('Key \'%s\' not found' % x)
        key_index = 0
        for x in self.original:
            index = dic.find(x)
            if index == -1:
                result += x
            else:
                index -= keys[key_index]
                index %= len(dic)
                result += dic[index]
            key_index += 1
            key_index %= len(keys)
        self.original = result
        if self.isundo == True:
            self.done.append(self.original)
    def vigenere(self, key, dic=dic) -> 'Vigenere Cipher decrypt':
        self.vigenere_cipher(key, dic)

string = '''
abcdefg
hijklmn
opq rst
uvw xyz

ABCDEFG
HIJKLMN
OPQ RST
UVW XYZ

12345
67890

+-*/=
()[]{}<>

This is a string type,
Isn't it?
Of cource yes! It is a string type.
'''

__test__ = False

# Test Decrypt for Python 2
if __test__ == True:
    a = Encrypt(string)
    print('get:')
    print(a.get())
    print
    a.caesar_cipher(5)
    print('caesar:')
    print(a.get())
    print
    a.reverse()
    print('reverse:')
    print(a.get())
    print
    a.undo()
    print('undo:')
    print(a.get())
    print
    a.vigenere_cipher('birthday')
    print('vigenere:')
    print(a.get())
    print
    a.reset()
    print('reset:')
    print(a.get())
    print
    a.set('abc')
    print('set:')
    print(a.get())
    print
    for x in range(3):
        a.undo()
    print('undo:')
    print(a.get())
    print
