class PlayerModel:
    def __init__(self, name):
        self.__name = name
        self.__hp = 100
        self.__alcohol_level = 0
        self.__x = 175
        self.__y = 175

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_alcohol_level(self):
        return self.__alcohol_level
    
    def set_x(self, value):
        self.__x = value

    def set_y(self, value):
        self.__y = value

    def set_alcohol_level(self, value):
        if value > 100:
            self.__alcohol_level = 100
        elif value < 0:
            self.__alcohol_level = 0
        else:
            self.__alcohol_level = value