'''
Created on 20. 7. 2019

@author: michal
'''

class Order(object):
    '''
    classdocs
    '''
    products=[]
    state=""
    orderId=""
    date=""
    
    def __init__(self, orderId, date, state, products):
        '''
        Constructor
        '''
        self.orderId = orderId
        self.date = date
        self.state = state
        self.products = products
        