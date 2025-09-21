# Performance-Testing with Apache JMeter & Flask

## Project Description

This project provides a web-based interface to run and manage Apache JMeter performance tests using a simple Flask application.
It allows users to input a target URL, execute load tests through JMeter in non-GUI mode, and view summarized results instantly in the browser. Test results are saved as CSV files, and users can also download raw JMeter logs for deeper analysis.

The goal of this project is to simplify performance testing by bridging backend automation with a user-friendly frontend interface.

---

## Features

* Web Interface for JMeter – Run tests from a browser without opening JMeter manually.
* Dynamic URL Input – Provide any website URL to test.
* Real-Time Summary – Get statistics like total requests, successes, errors, and success rate.
* Downloadable Reports – Export raw JMeter results in CSV format.
* Frontend Integration – Includes templates and a background image (`back.jpg`) for UI customization.
* Automated Test Runs – Executes JMeter with proper parameters (protocol, host, path).

---

## Tech Stack

* Python 3.x
* Flask – For the web server and API endpoints
* Apache JMeter 5.6.3 – Load testing engine
* HTML/CSS (Jinja Templates) – Web UI for inputs and results
* CSV Parsing – Summarizing test execution outcomes

---

## Project Structure

```
Performance-Testing/
│── app.py                # Flask application
│── back.jpg              # Background image for UI
│── jmeter.log            # Example JMeter execution log
│── templates/            # HTML templates
│── jmx_tests/            # JMeter test plans (JMX files)
│── results/              # Generated results (CSV exports)
```

---

## Getting Started

### Prerequisites

* Python 3.x
* Flask (`pip install flask`)
* Apache JMeter (installed and added to PATH)

### Clone the Repository

```bash
git clone https://github.com/Tharun-dot/Performance-Testing.git
cd Performance-Testing
```

### Configure Paths

Update **`app.py`** with your JMeter installation path:

```python
JMETER_PATH = r"C:\\Users\\apache-jmeter-5.6.3\\bin\\jmeter.bat"
JMX_FILE = r"C:\\Users\\apache-jmeter-5.6.3\\bin\\examples\\test-website.jmx"
RESULTS_DIR = r"C:\\Users\\apache-jmeter-5.6.3\\bin\\examples"
```

### Run the Flask App

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

### Usage

1. Enter a website URL in the input form.
2. Run the test – JMeter will execute with 10 threads (configurable in `.jmx`).
3. View summarized results instantly.
4. Download the detailed CSV report for analysis.

---

## Example JMeter Log

Sample run (`jmeter.log`) shows:

```
summary =    100 in 00:00:02 =   46.7/s Avg: 152 Min: 73 Max: 968 Err: 0 (0.00%)
```

100 requests executed successfully with no errors.

---

## Contributing

Pull requests are welcome.
For major changes, please open an issue first to discuss what you’d like to improve.

---

## License

This project is licensed under the MIT License.

---

> Web-based Performance Testing Tool powered by Apache JMeter & Flask
