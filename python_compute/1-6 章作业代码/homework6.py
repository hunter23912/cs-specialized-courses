class Person(object):
    def __init__(self, name = '', age = 20, sex = 'man'):
        self.setName(name)
        self.setAge(age)
        self.setSex(sex)

    def setName(self, name):
        if not isinstance(name, str):
            raise TypeError('name must be a string')
            print('name must be a string')
            return
        self.__name = name # __表示私有变量
        
    def setAge(self, age):
        if not isinstance(age, int):
            print('age must be an integer')
            return
        self.__age = age
    
    def setSex(self, sex):
        if sex != 'man' and sex != 'woman':
            print('sex must be "man" or "woman"')
            return
        self.__sex = sex
    def show(self):
        print('name:', self.__name)
        print('age:', self.__age)
        print('sex:',self.__sex)
        
class Student(Person):
    #调用基类构造方法初始化基类的私有数据成员
    def __init__(self, name='', age = 30, sex = 'man', major = 'Computer'):
        super(Student, self).__init__(name, age, sex)
        self.setMajor(major) #初始化派生类的数据成员
    
    def setMajor(self, major):
        if not isinstance(major, str):
            print('major must be a string.')
            return
        self.__major = major

    def show(self):
        super(Student, self).show()
        print('major:', self.__major)

Bob = Person('Zhang San', 19, 'man')
Bob.show()
Tom = Student('Li Si',32, 'man', 'Math')
Tom.show()