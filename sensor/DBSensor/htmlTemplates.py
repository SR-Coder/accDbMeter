
def htmlPage1(data):
    html = """<html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
            integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
            <style>
                html {
                    font-family: Arial;
                    display: inline-block;
                    margin: 0px auto;
                    text-align: center;
                }

                .button {
                    background-color: #ce1b0e;
                    border: none;
                    color: white;
                    padding: 16px 40px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    margin: 4px 2px;
                    cursor: pointer;
                }

                .button1 {
                    background-color: #000000;
                }
            </style>
        </head>

        <body>
            <h2> Raspberry Pi Pico Web Server</h2>
            <p>LED state: <strong>""" + data + """</strong></p>
            <p>
                <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
                <a href=\"?led_2_on\"><button class="button">LED ON</button></a>
            </p>
            <p>
                <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
                <a href=\"?led_2_off\"><button class="button button1">LED OFF</button></a>
            </p>
            <div>
                <form action="/login" method="post">
                    <div>
                        <label for="username">Username</label>
                        <input type="text" name="username" id="username" placeholder="username">
                    </div>
                    <div>
                        <label for="password">Password</label>
                        <input type="password" name="password" id="password" placeholder="password">
                    </div>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>

        </html>"""

    return html

def index(data = ""):
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ACC DB Sensor</title>
    </head>
        <body>
            <h1>Welcome and Login</h1>
            <div>
                <form action="/login" method="post">
                    <p>{}</p>
                    <div>
                        <label for="username">Username</label>
                        <input type="text" name="username" id="username" placeholder="username">
                    </div>
                    <div>
                        <label for="password">Password</label>
                        <input type="password" name="password" id="password" placeholder="password">
                    </div>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
    </html> 
    """ .format(data)
    return html

def dashboard():
    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>ACC DB Sensor</title>
        </head>
            <body>
                <h1>Welcome</h1>
                <div>
                    <p>HEY IT WORKED</p>
                </div>
            </body>
        </html>
    """
    return html