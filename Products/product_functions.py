from random import *

def count(n):
    n += 1

def getTotal(entries):
    total = 0
    for items in entries:
        total += items.price
    return total

class Guest:

    def __init__(self,guest_flag,visits,pk):
        self.guest_flag = guest_flag
        self.visits = visits
        self.username = self.gen_username()
        self.guest_id = self.gen_guest_id()
        self.pk = pk

    def guest_here(self):
        self.guest_flag = True



    def val_guest(self):
        self.guest_flag = True
        return self.guest_flag



    def gen_guest_id(self):
        guest_id = randint(4000, 100000)
        return str(guest_id)

    def gen_username(self):
        self.username = 'guest' + self.gen_guest_id()
        return self.username

    def count_visits(self):
        self.visits += 1
        return self.visits

    def create_guest_user(self,user):

        try:
            guestUser = user.objects.create_user(username=self.username)
            guestUser.save()
            print(guestUser.pk,'gregerg')
            self.pk = guestUser.pk
            return guestUser
        except:
           pass

    def get_guest(self, request):

        return request










