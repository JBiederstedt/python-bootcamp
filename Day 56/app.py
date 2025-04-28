from flask import Flask, render_template, url_for

app = Flask(__name__)

# Dummy data for the name card
dummy_data = {
    'name': 'John Doe',
    'title': 'Full-Stack Developer',
    'headline': 'Crafting amazing web experiences',
    'about': (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Vestibulum vehicula ex eu nisl facilisis, vitae convallis metus pulvinar."
    ),
    'email': 'john.doe@example.com',
    'phone': '+1 (555) 123-4567',
    'address': '1234 Elm Street, Anytown, USA',
    'social_links': {
        'github': '#',
        'linkedin': '#',
        'twitter': '#'
    }
}

@app.route('/')
def index():
    """
    Render the main page with dummy data.
    """
    # Pass all dummy_data keys into the template context
    return render_template('index.html', **dummy_data)

if __name__ == '__main__':
    # Debug mode for auto-reload and detailed errors
    app.run(debug=True)
