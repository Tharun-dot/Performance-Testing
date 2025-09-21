from flask import Flask, request, render_template, jsonify, send_from_directory
import subprocess
import os
import datetime
import csv
import platform
import urllib.parse

app = Flask(__name__)

# Get absolute path to project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# JMeter relative paths
JMETER_BIN = os.path.join(BASE_DIR, "apache-jmeter-5.6.3", "bin")
if platform.system() == "Windows":
    JMETER_PATH = os.path.join(JMETER_BIN, "jmeter.bat")
else:
    JMETER_PATH = os.path.join(JMETER_BIN, "jmeter")
    os.chmod(JMETER_PATH, 0o755)  # Ensure executable permission on Linux

JMX_FILE = os.path.join(BASE_DIR, "test-website.jmx")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_jmeter():
    url = request.form.get("url")
    if not url:
        return jsonify({"status": "error", "message": "No URL provided."})

    # Parse URL
    parsed_url = urllib.parse.urlparse(url)
    protocol = parsed_url.scheme
    host = parsed_url.netloc
    path = parsed_url.path or "/"

    # Generate unique results file name
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    results_file = os.path.join(RESULTS_DIR, f"results_{timestamp}.csv")
    
    # Build JMeter command
    jmeter_command = [
        JMETER_PATH,
        "-n",
        "-t", JMX_FILE,
        "-Jprotocol=" + protocol,
        "-Jhost=" + host,
        "-Jpath=" + path,
        "-l", results_file
    ]

    try:
        # Run JMeter
        result = subprocess.run(jmeter_command, capture_output=True, text=True)
        
        # Summarize CSV results
        total = success = error = 0
        if os.path.exists(results_file):
            with open(results_file, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    total += 1
                    if row.get("success") == "true":
                        success += 1
                    else:
                        error += 1

        return jsonify({
            "status": "success",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "results_file": f"/download/{os.path.basename(results_file)}",
            "summary": {
                "total": total,
                "success": success,
                "error": error,
                "success_rate": f"{(success/total*100 if total else 0):.2f}%"
            }
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(RESULTS_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
