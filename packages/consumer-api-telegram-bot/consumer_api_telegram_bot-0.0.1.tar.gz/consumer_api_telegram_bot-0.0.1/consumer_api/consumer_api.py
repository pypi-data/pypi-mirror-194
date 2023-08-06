from requests import post, get, put, delete


class ConsumerApi:

    def __init__(self, url: str, security_key: str) -> None:
        self.url = url
        self.headers = {"Content-Type": 'application/json',
                        "Authorization": security_key}

    def get_products(self):
        uri = f"{self.url}/product"
        request = get(uri, headers=self.headers)
        response = request.json()
        return response

    def get_product(self, product_id: str):
        uri = f"{self.url}/product/{product_id}"
        request = get(uri, headers=self.headers)
        response = request.json()
        return response

    def create_product(self, model_id: str, email: str, password: str):
        uri = f"{self.url}/product"
        body = {"model_id": model_id, "email": email, "password": password}
        request = post(uri, json=body, headers=self.headers)
        response = request.json()
        return response

    def delete_product(self, product_id: str):
        uri = f"{self.url}/product/{product_id}"
        request = delete(uri, headers=self.headers)
        response = request.json()
        return response

    def update_product(self, product_id: str, **kwargs):
        """
        Updates a product in the database.

        Args:
            model_id (str): The ID of the product model.
            email (str, optional): The email of product.
            password (str, optional): The password of product.
        """
        uri = f"{self.url}/product/{product_id}"
        request = put(uri, json=kwargs, headers=self.headers)
        response = request.json()
        return response

    def get_models(self):
        uri = f"{self.url}/model"
        request = get(uri, headers=self.headers)
        response = request.json()
        return response

    def get_model(self, model_id: str):
        uri = f"{self.url}/model/{model_id}"
        request = get(uri, headers=self.headers)
        response = request.json()
        return response

    def create_model(self, name: str, description: str, price: str):
        uri = f"{self.url}/model"
        body = {"name": name, "description": description, "price": price}
        request = post(uri, json=body, headers=self.headers)
        response = request.json()
        return response

    def delete_model(self, model_id: str):
        uri = f"{self.url}/model/{model_id}"
        request = delete(uri, headers=self.headers)
        response = request.json()
        return response

    def update_model(self, model_id: str, **kwargs):
        """
        Updates a model in the database.

        Args:
            name (str, optional)): The name of model.
            description (str, optional): The description of model.
            price (str, optional): The price of model.
        """
        uri = f"{self.url}/model/{model_id}"
        request = put(uri, json=kwargs, headers=self.headers)
        response = request.json()
        return response

    def get_client(self, client_id: str):
        uri = f"{self.url}/client/{client_id}"
        request = get(uri, headers=self.headers)
        response = request.json()
        return response

    def get_clients(self):
        uri = f"{self.url}/client"
        request = get(uri, headers=self.headers)
        response = request.json()
        return response

    def create_client(self, client_id: str):
        uri = f"{self.url}/client"
        body = {"id": client_id}
        request = post(uri, json=body, headers=self.headers)
        response = request.json()
        return response

    def add_balance(self, balance, client_id):
        uri = f"{self.url}/addbalance"
        body = {"balance": balance, "client_id": client_id}
        request = post(uri, json=body, headers=self.headers)
        response = request.json()
        return response

    def buy_product(self, product_id, client_id):
        uri = f"{self.url}/buyproduct"
        body = {"product_id": product_id, "client_id": client_id}
        request = post(uri, json=body, headers=self.headers)
        response = request.json()
        return response
