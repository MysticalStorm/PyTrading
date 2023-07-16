class Logger:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        print(scope)
        if scope['type'] == 'http':
            client = scope['client']
            method = scope['method']
            path = scope['path']
            params = ""
            # Printing query parameters
            if scope['query_string']:
                params = "?=" + scope['query_string'].decode()

            print(f"{client} - \"{method} {path}{params}\"")

            # Printing form parameters in the request body for POST requests
            if scope['method'] == 'POST':
                body = await receive()
                print(f"Body Parameters: {body['body'].decode()}")

        await self.app(scope, receive, send)