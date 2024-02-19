# Some Helper functions for the web server 

# Determine type of request
def getReqTypeAndRoute(request):
    try:
        get = request.find("b'GET")
        post = request.find("b'POST")

        if(get):
            # return the route 
            return {"get":get}
        if(post):
            # return the route
            return {"post": post}

    except OSError as e: 
        print("An error occured with the request: ", e)
        return {
            "get":get,
            "post":post
        }

    