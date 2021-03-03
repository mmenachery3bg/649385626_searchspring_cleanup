import json
with open("_cert_.json", "r") as write_file:
    lock_dict = json.load(write_file)
import http.client
import time

class BigCommerce_Connection:

    def __init__(self):
        self.store_hash = lock_dict['store_hash']   
        self.token = lock_dict["stitch-token"]   
        pass

    def setURL(self):
        self.url = f"https://api.bigcommerce.com/stores/{self.store_hash}/"

    def makeCall(self, call):
        """
        Making call to 
        """
        self.conn = http.client.HTTPSConnection("api.bigcommerce.com")
        self.headers = {'x-auth-token': self.token}
        self.conn.request(call, self.url, headers=self.headers)
    
    def getCall(self):
        """
        """
        self.makeCall('GET')
        res = self.conn.getresponse()
        data = res.read()
        self.data = json.loads(data.decode('utf-8'))
        self.meta = self.data['meta']
        self.data = self.data['data']
        pass

    def deleteCall(self):
        """
        """
        self.headers = {
                    'accept': "application/json",
                    'content-type': "application/json",
                    'x-auth-token': self.token
                    }
        self.makeCall('DELETE')
        pass

class Products(BigCommerce_Connection):

    def setProductListURL(self, next= '?limit=250&page=1'):
        """
        """
        self.url = f'https://api.bigcommerce.com/stores/{self.store_hash}/v3/catalog/products{next}'
        pass

    def setDeleteProduct(self, id):
        self.url = f'https://api.bigcommerce.com/stores/{self.store_hash}v3/catalog/products/{id}'
        pass
    


class Redirect(BigCommerce_Connection):


    def setURL(self, page, limit=250):
        """
        """
        self.url = f'https://api.bigcommerce.com/stores/{self.store_hash}/v3/storefront/redirects?page={page}&limit={limit}'
        self.token = lock_dict['redirect-token']
        pass

    def resetURLforDelete(self, id, site_id):
        """
        """
        self.url = f'https://api.bigcommerce.com/stores/{self.store_hash}/v3/storefront/redirects?site_id={site_id}&id%3Ain={id}'
        self.token = lock_dict['redirect-token']
        pass

    def getRedirectPage(self, page=1):
        """
        """
        self.setURL(page)
        self.getCall()
        self.disectData()
        self.number_of_pages= self.meta['pagination']['total_pages']
        pass

    def pullAllRedirects(self):
        """
        Pulling all redirect thru mulitple API calls
        """
        self.getRedirectPage() # first page
        
        list_ = self.data
        for page in range(1, self.number_of_pages):
            time.sleep(0.1)
            # print(len(list_), list_[-1])
            self.getRedirectPage(page=page+1)
            
            list_ += self.data
        self.list_of_redirect = list_
        pass

    def disectData(self):
        """
        """
        list_ = []
        for dict_ in self.data:
            transfer_dict = {}
            for key in ['id', 'site_id', 'from_path']:
                transfer_dict[key] = dict_[key] 
            for key in dict_['to'].keys():
                transfer_dict[key] = dict_['to'][key]
            list_ += [transfer_dict]
        self.data = list_
        pass


    def deleteRedirects(self, id, site_id):
        """
        Enter id and site_id, 
        """
        self.resetURLforDelete(id,site_id)
        self.deleteCall()
        pass





        




