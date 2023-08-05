
class SuperList(list):

    def reversed(self):
        return self[::-1]

    def cool_index(self, element):
        return self.index(element)
