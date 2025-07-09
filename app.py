from flask import Flask, render_template, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io, os, tempfile, uuid

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/remove-bg", methods=["POST"])
def remove_bg():
    img = request.files["image"]
    input_image = Image.open(img.stream).convert("RGBA")
    output = remove(input_image)

    # Use UUID for unique filename
    filename = f"{uuid.uuid4().hex}.png"
    path = os.path.join(tempfile.gettempdir(), filename)
    
    # Save image manually to avoid Windows issues
    output.save(path)

    return jsonify({"filename": filename})

@app.route("/result/<filename>")
def show_result(filename):
    path = os.path.join(tempfile.gettempdir(), filename)
    if not os.path.exists(path):
        return "File not found or expired", 404
    return send_file(path, mimetype="image/png")

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    try:
        path = os.path.join(tempfile.gettempdir(), filename)
        if os.path.exists(path):
            os.remove(path)
            return jsonify({"status": "deleted"})
        else:
            return jsonify({"status": "already deleted"})
    except:
        return jsonify({"status": "failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
