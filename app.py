from flask import Flask, request, render_template, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JMETER_PATH = os.path.join(BASE_DIR, "apache-jmeter-5.6.3", "bin", "jmeter")
JMX_FILE = os.path.join(BASE_DIR, "test-website.jmx")
RESULTS_FILE = os.path.join(BASE_DIR, "results.csv")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_jmeter():
    try:
        # Run JMeter command
        result = subprocess.run(
            [JMETER_PATH, "-n", "-t", JMX_FILE, "-l", RESULTS_FILE],
            capture_output=True,
            text=True
        )
        return jsonify({
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "results_file": "/download/results.csv"
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(BASE_DIR, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
