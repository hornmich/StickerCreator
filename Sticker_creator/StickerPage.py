'''
Created on 9. 7. 2019

@author: michal
'''

class StickerPage:
    '''
    Sticker page constructor.
    '''
    tempatePage = ''
    TIMGPREFIX='ST_IMG_'
    TLBLPREFIX='ST_LBL_'
    
    def __init__(self, templateFile) :
        '''
        Create new sticker constructor by using given HTML template.
        '''
        with open(templateFile) as template:
            self.tempatePage = template.read();
            template.close()
            
    def putSticker(self, index, item):
        '''
        Insert sticker on a position given by index.
        '''
        image=item[1]
        label=item[0]
        index_str='{0:02d}'.format(index)
        timgkey=self.TIMGPREFIX+index_str
        tlblkey=self.TLBLPREFIX+index_str
        self.tempatePage = self.tempatePage.replace(timgkey, image)
        self.tempatePage = self.tempatePage.replace(tlblkey, label)
        
    def clearSticker(self, index):
        '''
        Remove sticker from position given by index.
        '''
        image=''
        label=''
        index_str='{0:02d}'.format(index)
        timgkey=self.TIMGPREFIX+index_str
        tlblkey=self.TLBLPREFIX+index_str
        self.tempatePage = self.tempatePage.replace(timgkey, image)
        self.tempatePage = self.tempatePage.replace(tlblkey, label)
        
    def save(self, fileName):
        '''
        Save this stickers to a file.
        '''
        with open(fileName, 'w') as result:
            result.write(self.tempatePage)
            result.close()