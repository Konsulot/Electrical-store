from concurrent import futures
import grpc
import user_pb2
import user_pb2_grpc

users = [
    {"id": 1, "username": "user1", "password": "password1"},
    {"id": 2, "username": "Ivan", "password": "Konsul"},
    {"id": 3, "username": "user3", "password": "password3"},
]

class UserService(user_pb2_grpc.UserServiceServicer):
    def Authenticate(self, request, context):
        for user in users:
            if user["username"] == request.username and user["password"] == request.password:
                return user_pb2.AuthResponse(user_id=user["id"], message="Success")
        return user_pb2.AuthResponse(user_id=0, message="Invalid username or password")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
