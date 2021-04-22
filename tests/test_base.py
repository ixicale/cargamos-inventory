"""Application test"""

# Utils
import unittest
import json

# Aplicación
from app import app
from application import db



class AppTest(unittest.TestCase):
    """application test case"""

    def setUp(self):
        """Set up application' DB & APP"""
        self.app = app.test_client()
        self.db = db.get_db()

    def test_successful_post_to_product(self):
        """Test 'Create new product'"""
        payload = json.dumps({
            "sku": 1151,
            "product": "Procesador Intel Core i9"
        })
        response = self.app.post(
            '/product', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_get_product(self):
        """Test 'Display all products records'"""
        response = self.app.get('/product')
        self.assertEqual(200, response.status_code)
    
    def test_successful_get_specific_product(self):
        """Test 'Retuns first item by SKU'"""
        response = self.app.get('/product/1151')
        self.assertEqual(200, response.status_code)
    
    def test_successful_patch_specific_product(self):
        """Test 'Update product record'"""
        payload = json.dumps({
            "product": "Ryzen 5 3400G"
        })
        response = self.app.patch(
            '/product/1151', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_post_to_store(self):
        """Test 'Add new store'"""
        payload = json.dumps({
            "store": "Digitallife",
            "address": "Av. Adolfo López Mateos Sur 5510"
        })
        response = self.app.post(
            '/tiendas', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_get_store(self):
        """Test 'Display all store records'"""
        response = self.app.get('/tiendas')
        self.assertEqual(200, response.status_code)
    
    def test_successful_get_specific_store(self):
        """Test 'Retuns first store by ID'"""
        response = self.app.get('/tiendas/1')
        self.assertEqual(200, response.status_code)
    
    def test_successful_patch_specific_store(self):
        """Test 'Update store record'"""
        payload = json.dumps({
            "store": "DDTech"
        })
        response = self.app.patch(
            '/tiendas/1', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_post_to_stock(self):
        """Test 'Update stock by store ID and SKU'"""
        payload = json.dumps({
            "store_id": 1,
            "product_sku": 1151,
            "minimum": 5,
            "stock": 3
        })
        response = self.app.post(
            '/stock', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_get_insufficient_stock(self):
        """Test 'Returns the list of insufficient product stocks list by store'"""
        response = self.app.get('/tiendas/1/stock/insufficient')
        self.assertEqual(200, response.status_code)
    
    def test_successful_patch_stock_from_store(self):
        """Test 'Update just stock by store'"""
        payload = json.dumps({
            "stock": 6
        })
        response = self.app.post(
            '/tiendas/1/stock/1151', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)

    def test_successful_delete_specific_product(self):
        """Test 'Delete product record'"""
        response = self.app.delete('/product/1151')
        self.assertEqual(204, response.status_code)

    def test_successful_delete_specific_store(self):
        """Test 'Delete store record'"""
        response = self.app.delete('/tiendas/1')
        self.assertEqual(204, response.status_code)