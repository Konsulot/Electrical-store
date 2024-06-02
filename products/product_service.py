from concurrent import futures
import grpc
import product_pb2
import product_pb2_grpc

products = {
    product_pb2.ProductCategory.MOBILE: [
        {"id": 1, "title": "iPhone 12", "description": "Последняя модель iPhone с 5G, 64GB памяти, цвет черный", "price": 800.00},
        {"id": 2, "title": "Samsung Galaxy S21", "description": "Флагманский телефон Samsung с отличной камерой, 128GB памяти, цвет серебристый", "price": 1000.00},
        {"id": 3, "title": "Google Pixel 5", "description": "Последний смартфон от Google с 8GB оперативной памяти, 128GB встроенной памяти, цвет зелёный", "price": 700.00},
        {"id": 8, "title": "OnePlus 9", "description": "Смартфон OnePlus с 12GB оперативной памяти, 256GB встроенной памяти, цвет синий", "price": 750.00},
        {"id": 9, "title": "Xiaomi Mi 11", "description": "Телефон Xiaomi с 108MP камерой, 256GB памяти, цвет белый", "price": 650.00},
        {"id": 14, "title": "Huawei P40 Pro", "description": "Флагманский смартфон с поддержкой 5G, 8GB оперативной памяти, 256GB встроенной памяти, цвет черный", "price": 900.00},
        {"id": 15, "title": "Sony Xperia 5", "description": "Компактный смартфон с 6.1-дюймовым экраном, 8GB оперативной памяти, 128GB встроенной памяти, цвет синий", "price": 800.00},
        {"id": 16, "title": "HONOR Magic6 Pro", "description": "Смартфон с 120Hz дисплеем, 12GB оперативной памяти, 256GB встроенной памяти, цвет мятный", "price": 950.00},
    ],
    product_pb2.ProductCategory.LAPTOP: [
        {"id": 4, "title": "MacBook Pro", "description": "Мощный ноутбук от Apple с процессором M1, 16GB оперативной памяти, 512GB SSD, цвет серебристый", "price": 1300.00},
        {"id": 5, "title": "Dell XPS 13", "description": "Компактный и мощный ноутбук с процессором Intel i7, 16GB оперативной памяти, 1TB SSD, цвет чёрный", "price": 1000.00},
        {"id": 10, "title": "HP Spectre x360", "description": "Ультрабук-трансформер с сенсорным экраном, процессором Intel i7, 16GB оперативной памяти, 512GB SSD, цвет синий", "price": 1200.00},
        {"id": 11, "title": "Lenovo ThinkPad X1 Carbon", "description": "Бизнес-ноутбук с процессором Intel i7, 16GB оперативной памяти, 1TB SSD, цвет чёрный", "price": 1400.00},
        {"id": 17, "title": "Asus ROG Zephyrus G14", "description": "Игровой ноутбук с процессором AMD Ryzen 9, 16GB оперативной памяти, 1TB SSD, цвет белый", "price": 1500.00},
        {"id": 18, "title": "Microsoft Surface Laptop 4", "description": "Ноутбук с сенсорным экраном, процессором Intel i7, 16GB оперативной памяти, 512GB SSD, цвет платиновый", "price": 1300.00},
        {"id": 19, "title": "Acer Swift 3", "description": "Легкий и тонкий ноутбук с процессором AMD Ryzen 7, 8GB оперативной памяти, 512GB SSD, цвет серебристый", "price": 800.00},
    ],
    product_pb2.ProductCategory.CAMERA: [
        {"id": 6, "title": "Canon EOS R5", "description": "Высококлассная беззеркальная камера с 45MP сенсором, поддержка 8K видео, цвет чёрный", "price": 3900.00},
        {"id": 7, "title": "Sony Alpha a7 III", "description": "Универсальная полнокадровая камера с 24MP сенсором, поддержка 4K видео, цвет чёрный", "price": 2000.00},
        {"id": 12, "title": "Nikon Z6 II", "description": "Беззеркальная камера с 24.5MP сенсором, поддержка 4K видео, цвет чёрный", "price": 2100.00},
        {"id": 13, "title": "Fujifilm X-T4", "description": "Камера с 26.1MP сенсором, поддержка 4K видео, цвет серебристый", "price": 1700.00},
        {"id": 20, "title": "Panasonic Lumix GH5", "description": "Камера с 20.3MP сенсором, поддержка 4K видео, цвет чёрный", "price": 1500.00},
        {"id": 21, "title": "Olympus OM-D E-M1 Mark III", "description": "Камера с 20.4MP сенсором, поддержка 4K видео, цвет чёрный", "price": 1800.00},
        {"id": 22, "title": "Leica Q2", "description": "Компактная камера с 47.3MP сенсором, поддержка 4K видео, цвет чёрный", "price": 5000.00},
    ],
}


class ProductService(product_pb2_grpc.ProductServiceServicer):
    def GetProducts(self, request, context):
        category = request.category
        return product_pb2.ProductListResponse(products=products[category])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    product_pb2_grpc.add_ProductServiceServicer_to_server(ProductService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
