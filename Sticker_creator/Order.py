'''
Created on 9. 7. 2019

@author: michal
'''
import xmltodict
import urllib
import re
import html

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
        with urllib.request.urlopen(url) as fd:
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
