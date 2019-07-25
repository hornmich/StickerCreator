'''
Created on 20. 7. 2019

@author: michal
'''

class OrderItem(object):
    '''
    classdocs
    '''
    imgurl=""
    label=""

    def __init__(self, imgurl, label):
        '''
        Constructor
        '''
        self.imgurl = imgurl
        self.label = label
        
    def __str__(self, *args, **kwargs):
        return self.label
        