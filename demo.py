import requests
import webbrowser

# CHANGE THE VARIABLE BELOW TO YOUR FLASK URL
FLASK_URL = "http://localhost:8080"


def http(method, path, data=None):
    print(f"Making {method} request to {FLASK_URL + path}...")
    if method not in ["GET", "POST", "PUT", "DELETE"]:
        raise RuntimeWarning("Invalid method")
    
    if method == "GET":
        response = requests.get(FLASK_URL + path)
    elif method == "POST":
        response = requests.post(FLASK_URL + path, json=data)
    elif method == "PUT":
        response = requests.put(FLASK_URL + path, json=data)
    elif method == "DELETE":
        response = requests.delete(FLASK_URL + path)
    
    print("Received status code:", response.status_code)
    return response

def get(path):
    return http("GET", path)


def post(path, data=None):
    return http("POST", path, data)


def put(path, data=None):
    return http("PUT", path, data)


def delete(path):
    return http("DELETE", path)


def demo():
    print("Adding a new product: 'Bacon' (6.99)")
    post("/api/products", {"name": "Bacon", "price": 6.99, "available": 0})
    post("/api/products", {"name": "Chips", "price": 5.63, "available": 20})
    post("/api/products", {"name": "Sushi", "price": 8.96, "available": 15})
    input("Check for salty nuts in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/products")
    input("Press Enter to continue.")
    post("/api/orders", {"customer_id": 20, "items": [{"name": "Bacon", "quantity": 16}]})
    input("Check for the order in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")
    post("/api/orders", {"customer_id": 19, "items": [{"name": "Chips", "quantity": 25}]})
    input("Check for the order in the web page. Press Enter when ready.")
    # webbrowser.open(FLASK_URL + "/orders")
    input("Press Enter to continue.")
    post("/api/orders", {"customer_id": 18, "items": [{"name": "Sushi", "quantity": 10}]})


if __name__ == "__main__":
    demo()
