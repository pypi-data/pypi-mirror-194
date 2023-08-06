import random

from enum import Enum


class Color( Enum ) :
    Green = 0
    Red = 1
    Black = 2


class Slot:
    def __init__(self, color, number):
        self.color = None
        self.number = number


class Wheel:
    def __init__(self, size=36, number_of_reds=18, number_of_blacks=18, number_of_greens=2):
        self.size = size
        self.number_of_reds = number_of_reds
        self.number_of_blacks = number_of_blacks
        self.number_of_greens = number_of_greens
        self.wheel_size = number_of_reds + number_of_blacks + number_of_greens
        self.black_slots = []
        self.red_slots = []
        self.green_slots = []
        self.slots = []
        self.create_wheel()

        """
        :brief: A very ugly construction.
        
        :details: The model is made up of 36 slots. Each slot is made up of a color and a number.
        1.) Every other slot starting from 1 is a red slot.
        
        2.) Every other slot starting from 2 is a black slot.
        
        3.) The 
        
        Combine all these lists into one giant list representing the model. That's where random will draw from.
        
        :TODO: For custom wheels, it's unsafe to assume the number of green slots.
        """
        for i in list( range( 1, self.wheel_size, 2 ) ) :
            self.red_slots.append( Slot( Color.Red, i ) )

        # TODO: find a better way to do this
        for i in self.red_slots:
            i.color = Color.Red

        for i in list( range( 0, self.wheel_size, 2 ) ) :
            self.black_slots.append( Slot( Color.Black, i ) )

        # TODO: find a better way to do this
        for i in self.black_slots:
            i.color = Color.Black

        self.black_slots[0].color = Color.Green
        self.red_slots[-1].color = Color.Green

        self.slots = self.black_slots + self.red_slots + self.green_slots

    def random_spin(self):
        return random.choice(self.slots)

    def create_wheel( self ) :
        # TODO I doubt this will work
        pass