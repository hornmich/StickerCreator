'''
Created on 9. 7. 2019

@author: michal
'''
import xmltodict
import urllib
import re
import html
from Sticker_creator import OrderItem
from Sticker_creator import Order

class Orders:
    '''
    Eshop-rychle map of products images and names from exported order.
    '''
    shopProducts = []
    orders=[]
    
    def __init__(self, shopProductsUrl, orderProductsUrl) :
        '''
        Construct list of tuples containing order product names and images url.
        '''
        self.shopProducts = self.loadShopProducts(shopProductsUrl)
        self.orders = self.loadOrders(orderProductsUrl)

    def loadShopProducts(self, url):
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

    def loadOrders(self, url):
        orders = []
        with urllib.request.urlopen(url) as fd:
            xmlOrders = xmltodict.parse(fd.read())['orders']['order']
            if (type(xmlOrders) != list):
                print('\tConverting orders into list.')
                xmlOrders = [xmlOrders]
            for xmlOrder in xmlOrders:
                order = self.loadOrder(xmlOrder)
                orders.append(order)
        return orders
                
          
    def loadOrder(self, xml):
        state = xml['info']['lastState']
        orderId = xml['info']['orderID']
        date = xml['info']['date']
        xmlProducts=xml['products']['product']
        products = self.loadProducts(xmlProducts)
        return Order.Order(orderId, date, state, products)
            
    def loadProducts(self, xml):
        products = []
        if (type(xml) != list):
            print('\tConverting products into list.')
            xml = [xml]
            
        for xmlProduct in xml:
            prod_name=html.unescape(xmlProduct['name'])
            if prod_name == 'Slevový kupón / Dárkový šek':
            	print('Přeskakuiji kupon.')
            	continue
            cnt=int(xmlProduct['pieces'])
            print('\t\t{0} products in order.'.format(cnt))
            index = re.search("[0-9]\ *ks", html.unescape(xmlProduct['name']))
            prod=xmlProduct['name'][:index.end()]
            print('\t\t{0}->{1}[0-{2}]->{3}'.format(xmlProduct['name'], prod_name, index.end(), prod))
            if (prod != ''):
                for i in range(0, cnt):
                    print('\t\t\t{0} - adding product {1}'.format(str(i), prod))
                    if (prod in self.shopProducts) :
                        print('\t\tImage ', self.shopProducts[prod])
                        products.append(OrderItem.OrderItem(self.shopProducts[prod], prod)) 
                    else:
                        ''' Image not found for this item '''
                        pass
            else:
                ''' invalid name of product '''
                pass
        return products
            