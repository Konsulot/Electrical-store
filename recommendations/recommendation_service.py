from concurrent import futures
import grpc
import random
import recommendation_pb2
import recommendation_pb2_grpc
import product_pb2
import product_pb2_grpc

products = {
    product_pb2.ProductCategory.MOBILE: [
        {"id": 1, "title": "iPhone 12", "description": "Latest model iPhone with 5G", "price": 800.00},
        {"id": 2, "title": "Samsung Galaxy S21", "description": "Flagship Samsung phone with amazing camera", "price": 1000.00},
        {"id": 3, "title": "Google Pixel 5", "description": "Google's latest smartphone", "price": 700.00},
    ],
    product_pb2.ProductCategory.LAPTOP: [
        {"id": 4, "title": "MacBook Pro", "description": "Powerful laptop from Apple", "price": 1300.00},
        {"id": 5, "title": "Dell XPS 13", "description": "Compact and powerful laptop", "price": 1000.00},
    ],
    product_pb2.ProductCategory.CAMERA: [
        {"id": 6, "title": "Canon EOS R5", "description": "High-end mirrorless camera", "price": 3900.00},
        {"id": 7, "title": "Sony Alpha a7 III", "description": "Versatile full-frame camera", "price": 2000.00},
    ],
}

class RecommendationService(recommendation_pb2_grpc.RecommendationServiceServicer):
    def Recommend(self, request, context):
        category = request.category
        num_results = min(request.max_results, len(products[category]))
        recommendations = random.sample(products[category], num_results)
        return recommendation_pb2.RecommendationResponse(products=recommendations)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendation_pb2_grpc.add_RecommendationServiceServicer_to_server(RecommendationService(), server)
    server.add_insecure_port("[::]:50053")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
