import random
import string
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    generated_password = ""
    error_message = ""
    
    # Track inputs so checkboxes stay checked after clicking the button
    include_numbers = True
    include_symbols = True
    length = 12
    
    if request.method == "POST":
        length = int(request.form.get("length", 12))
        
        # Check if the checkboxes were selected (returns 'yes' if checked, None if empty)
        include_numbers = request.form.get("numbers") == "yes"
        include_symbols = request.form.get("symbols") == "yes"
        
        # Core character pool: Always include letters
        characters = string.ascii_letters
        
        # Dynamically append character pools based on checkboxes
        if include_numbers:
            characters += string.digits
        if include_symbols:
            characters += string.punctuation
            
        # Error handling: If user turned off numbers AND symbols, ensure pool isn't broken
        if not characters:
            error_message = "Error: Please keep at least one character type checked!"
        else:
            generated_password = "".join(random.choice(characters) for _ in range(length))
    
    return render_template(
        "index.html", 
        password=generated_password,
        error_message=error_message,
        current_length=length,
        include_numbers=include_numbers,
        include_symbols=include_symbols
    )

if __name__ == "__main__":
    app.run(debug=True)
