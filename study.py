#!/usr/bin/python3
import glob
import pymysql
from timeit import Timer
class c1():
    name =''
    age =0
    __weight =0
    def __init__(self, n,a,w):
        self.name =n
        self.age = a
        self.__weight =w

    def speak(self):
        print("%s说：我%d岁。" %(self.name,self.age))


class c2(c1):
    grade = ''
    def __init__(self, n,a,w,g):
        c1.__init__(self,n,a,w)
        self.grade = g

    def speak(self):
        print("%s 说：我%d岁了，我在读%d年级"%(self.name,self.age,self.grade))

class c3():
    topic =''
    name =''
    def __init__(self, n,t):
        self.name =n
        self.topic =t

    def speak(self):
        print("我叫%s，我是一个演说家，我演讲的主题是%s"%(self.name,self.topic))


class c4(c3,c2):
    a =''
    def __init__(self, n,a,w,g,t):
        c2.__init__(self,n,a,w,g)
        c3.__init__(self,n,t)


test = c4("tim",25,80,4,"python")
test.speak()


class Site:
    name =''
    __email=''
    def __init__(self,name,email):
        self.name=name
        self.__email = email

    def who(self):
        print("name:",self.name)
        print("email:",self.__email)


    def __foo(self):
        print("这是私有方法")

    def foo(self):
        print("这是公共方法")

x = Site("唐",'840733587@qq.com')
x.who()
x.foo()
print(glob.glob('*.py'))

