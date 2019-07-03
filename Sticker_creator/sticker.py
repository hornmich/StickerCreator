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

import xmltodict
import urllib
import re
import html
import os

class Order:
    '''
    Eshop-rychle map of products images and names from exported order.
    '''
    shopProductsUrl=''
    orderProductsUrl=''
    shop_prods_imgs={}
    order_prods_imgs=[]
    order_prods=[]
    
    def __init__(self, shopProductsUrl, orderProductsUrl) :
        '''
        Construct list of tuples containing order product names and images url.
        '''
        self.shopProductsUrl=shopProductsUrl
        self.orderProductsUrl=orderProductsUrl
        self.shop_prods_imgs=self.getShopProdsImgs(self.shopProductsUrl)
        self.order_prods=self.getOrderProducts(self.orderProductsUrl)
        self.order_prods_imgs=self.getOrderProdsImgs(self.shop_prods_imgs, self.order_prods)

    def getShopProdsImgs(self, url):
        '''
        Construct dictionary of all shop products names and their images url.
        '''
        shop_products={}
        print('Making dictionary of products and images from eshop portfolio.')
        with urllib.request.urlopen(url) as fd:
            doc = xmltodict.parse(fd.read())
            for product in doc['SHOP']['SHOPITEM']:
                prod_name=html.unescape(product['PRODUCTNAME'])
                print('\tProduct {0} -> {1} : {2}'.format(product['PRODUCTNAME'], prod_name, product['IMGURL']))
                shop_products[prod_name] = product['IMGURL']
        return shop_products

    def getOrderProducts(self, url):
        '''
        Return a list of product names, extracted from Eshop-rychle exported orders.
        '''
        order_products=[]
        with open(url) as fd:
            print('Making list of products names in order.')
            orders = xmltodict.parse(fd.read())['orders']['order']
            if (type(orders) != list):
                print('\tConverting orders into list.')
                orders = [orders]

            for order in orders:
                products=order['products']['product']
                if (type(products) != list):
                    print('\tConverting products into list.')
                    products = [products]
                    
                for product in products:
                    cnt=int(product['pieces'])
                    print('\t\t{0} products in order.'.format(cnt))
                    prod_name=html.unescape(product['name'])
                    index = re.search("[0-9]\ *ks", html.unescape(product['name']))
                    prod=product['name'][:index.end()]
                    print('\t\t{0}->{1}[0-{2}]->{3}'.format(product['name'], prod_name, index.end(), prod))
                    if (prod != ''):
                        for i in range(0, cnt):
                            print('\t\t\t{0} - adding product {1}'.format(str(i), prod))
                            order_products.append(prod)
        return order_products

    def getOrderProdsImgs(self, shop_products, order_products):
        '''
        Return list of tuples, containing order product names and its images.
        '''
        products=[]
        print('Making dictionary of products names in order and images.')
        for prod in order_products:
            print('\tProduct '+prod)
            if (prod in shop_products) :
                print('\t\tImage ', shop_products[prod])
                products.append((prod, shop_products[prod]))
        return products

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

class ConsoleStickerCreator:
    def loadOrderProducts(self):
        feedXmlUrl=input('Heureka URL feed (nebo Enter pro vychozi): ') or 'https://www.vzorkyplenek.cz/fotky74713/xml/heureka_cz.xml'
        orderXmlUrl=input('Objednavky URL: ')  or '5b08d8e9af1c6d7d73bf6d9d48e5d9ab.xml'
        
        order = Order(feedXmlUrl, orderXmlUrl)
        print(order.shop_prods_imgs)
        print(order.order_prods)
        print(order.order_prods_imgs)
        products=order.order_prods_imgs
        return products
        
    def createStickerPage(self, indexes, products, fileName):     
        usedIndexes=[]
        print('Nacitam sablonu.')
        stickerPage=StickerPage('template.html')
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
        if os.system('wkhtmltoimage --format png --quality 100 -q '+fileName+' '+fileName+'.png') != 0 :
            print('Conversion failed.')
        print('Stitky ulozeny. {0} polozek zbyva.'.format(leftCnt))
        if (leftCnt > 0):
            cont=input('Vytvorit nove stitky (a/n)? ')
        else :
            cont='n'

        cnt=cnt+1
    print('Hotovo')
