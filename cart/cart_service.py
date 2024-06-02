from concurrent import futures
import grpc
from cart_pb2 import CartResponse, AddItemRequest, RemoveItemRequest, GetCartRequest, CartStatus, CartItem
import cart_pb2_grpc

# This is a simple in-memory store for the carts.
carts = {}


class CartService(cart_pb2_grpc.CartServiceServicer):
    def AddItem(self, request, context):
        cart_id = request.cart_id
        item = request.item

        if cart_id not in carts:
            carts[cart_id] = {
                "items": [],
                "status": CartStatus.ACTIVE
            }

        # Check if the item already exists in the cart
        existing_item = next((i for i in carts[cart_id]["items"] if i.id == item.id), None)
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            carts[cart_id]["items"].append(item)

        return CartResponse(cart_id=cart_id, items=carts[cart_id]["items"], status=carts[cart_id]["status"])

    def RemoveItem(self, request, context):
        cart_id = request.cart_id
        item_id = request.item_id

        if cart_id in carts:
            carts[cart_id]["items"] = [item for item in carts[cart_id]["items"] if item.id != item_id]

        return CartResponse(cart_id=cart_id, items=carts[cart_id]["items"], status=carts[cart_id]["status"])

    def GetCart(self, request, context):
        cart_id = request.cart_id
        if cart_id in carts:
            return CartResponse(cart_id=cart_id, items=carts[cart_id]["items"], status=carts[cart_id]["status"])
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Cart not found")
            return CartResponse()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cart_pb2_grpc.add_CartServiceServicer_to_server(CartService(), server)
    server.add_insecure_port("[::]:50054")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
