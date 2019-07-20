'''
Command line script for composing stickers of diapers.

The script allows to import complete list of products from feed XML
file for heureka.cz and XML file with orders from eshop-rychle shop.

The script filters out and merges together name of the product and its
image and puts it into a HTML based table for 3*8 A4 form factor sticker
list, leaving the rest blank.

The script allows to process the order by one or more batches, to
optimize usage of sticker lists.

Created on 15. 6. 2019

@author: Michal Horn
@todo: Automatic page fill clear empty stickers
@todo: Last one always left uncleared
@todo: Make orders load from url
@todo: Reorganize directories to have CSS and template on the same place as generator
@todo: Call to image converter
@todo: Add borders to page
@todo: automatically crop image
'''

import os
from Sticker_creator import Order
from Sticker_creator import StickerPage

class ConsoleStickerCreator:
    def loadOrderProducts(self):
        feedXmlUrl=input('Heureka URL feed (nebo Enter pro vychozi): ') or 'https://www.vzorkyplenek.cz/fotky74713/xml/heureka_cz.xml'
        orderXmlUrl=input('Objednavky URL: ')
        
        order = Order.Order(feedXmlUrl, orderXmlUrl)
        print(order.shop_prods_imgs)
        print(order.order_prods)
        print(order.order_prods_imgs)
        products=order.order_prods_imgs
        return products
        
    def createStickerPage(self, indexes, products, fileName):     
        usedIndexes=[]
        print('Nacitam sablonu.')
        stickerPage=StickerPage.StickerPage('template.html')
        for index in indexes:
            if (not products):
                break
            prod = products.pop(0)
            index = int(index)
            print('Pridavam stitek {0} s produktem {1}'.format(index, prod))
            stickerPage.putSticker(index, prod)
            usedIndexes.append(int(index))
        
        # Clear all that were not added
        allIndexes=list(range(1,25))
        emptySticks=[x for x in allIndexes if x not in usedIndexes]
        
        print('Mazu policka '+str(emptySticks))
        for emptyStick in emptySticks:
            stickerPage.clearSticker(emptyStick)
       
        stickerPage.save(fileName)
        leftCnt = len(products)
        return leftCnt

if __name__ == '__main__':
    stickerCreator=ConsoleStickerCreator()
    products=stickerCreator.loadOrderProducts()
    cont='a'
    cnt=1
    while (cont == 'a'):
        indexes = (input('Cisla stitku oddelena mezerou (nebo Enter pro vychozi): ') or '1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24').split(' ')
        fileName = input('Ulozit jako (nebo Enter pro vychozi): ') or str.format('out{0}.html', cnt) 
        leftCnt = stickerCreator.createStickerPage(indexes, products, fileName)
        print('Prevadim na obrazek.')
        if os.system('wkhtmltoimage --format png --quality 100 --crop-y 50 --crop-x 30 --crop-w 980 --crop-h 1450 -q '+fileName+' '+fileName+'.png') != 0 :
            print('Conversion failed.')
        print('Stitky ulozeny. {0} polozek zbyva.'.format(leftCnt))
        if (leftCnt > 0):
            cont=input('Vytvorit nove stitky (a/n)? ')
        else :
            cont='n'

        cnt=cnt+1
    print('Hotovo')
