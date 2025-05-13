from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    images = [
        'https://cdn.prod.website-files.com/6009ec8cda7f305645c9d91b/65c183700d8fbc2492a6c314_6531361ccf5757c2e991e9fb_6pWiS1br6sImopelr9oFycse8XLyhAhsekWbiO9joSDCA1C1A8WdoqGUwSQ27hdFGHSQLYcPNW6LbG0Mj-y0shVQpObaToGnAWatUFwUItJYcEGgpcPj4A-RMiEubBUsOMT5qMlTw5n2wnsvvbA9pHo.png',
        'https://www.zarla.com/images/zarla-it-website-examples-3840x2400-20240730.webp?crop=4:3,smart&width=1200&dpr=2',
        'https://cdn.cmsfly.com/635bcad9b8a74e0091632998/image-ZI9Na7.png'
    ]
    return render_template('index.html', images=images)

if __name__ == '__main__':
    app.run(debug=True)
