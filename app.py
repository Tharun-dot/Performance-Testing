from flask import Flask, request, render_template, jsonify, send_from_directory
import subprocess
import os
import datetime
import csv
import urllib.parse # Import the urllib.parse module

app = Flask(__name__)

JMETER_PATH = r"C:\\Users\\apache-jmeter-5.6.3\\bin\\jmeter.bat"
JMX_FILE = r"C:\\Users\\apache-jmeter-5.6.3\\bin\\examples\\test-website.jmx"
RESULTS_DIR = r"C:\\Users\\apache-jmeter-5.6.3\\bin\\examples"

os.makedirs(RESULTS_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_jmeter():
    url = request.form.get("url")
    if not url:
        return jsonify({"status": "error", "message": "No URL provided."})

    # Use urllib.parse to split the URL into components
    parsed_url = urllib.parse.urlparse(url)
    protocol = parsed_url.scheme
    host = parsed_url.netloc
    path = parsed_url.path
    if not path:
        path = "/"

    # Generate a unique results file name to avoid conflicts
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    results_file = os.path.join(RESULTS_DIR, f"results_{timestamp}.csv")
    
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
        # Run the JMeter command
        result = subprocess.run(jmeter_command, capture_output=True, text=True)
        
        # Read the generated CSV file and summarize results
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