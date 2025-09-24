from opcua import Client


class OpcClient:
    def __init__(self, url: str, username: str = None, password: str = None) -> None:

        self.client = Client(url)
        if username and password:
            self.client.set_user(username)
            self.client.set_password(password)

        try:
            self.client.connect()
        except Exception as e:
            print(f"Error in conection to OPC Server: {e}")

    def setValue(self, nodeTag: str, newValue):
        try:
            self.client.get_node(
                f"ns=2;s={nodeTag}").set_value(float(newValue))
        except Exception as e:
            pass

    def getValue(self, nodeTag: str) -> float:
        return self.client.get_node(f"ns=2;s={nodeTag}").get_value()
    
    # def Know(self):
        
    #     return node