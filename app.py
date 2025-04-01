from flask import Flask, render_template, Response
from flask import Flask, jsonify, make_response
from flask import make_response, render_template
import weasyprint
import json
import sqlite3
import pandas as pd
from io import BytesIO

app = Flask(__name__)

DB_NAME = "/home/kevinchriste/madison_project/census_data.db"
TABLE_NAME = "state_population"

def get_results():
    """Fetch the calculated representation results from the database."""
    conn = sqlite3.connect(DB_NAME)
    query = f"SELECT * FROM {TABLE_NAME}"
    df = pd.read_sql(query, conn)
    conn.close()

    # Calculate representatives
    results = []
    for _, row in df.iterrows():
        state = row["state_name"]
        population = row["population"]

        if population < 30000:
            reps = 1
        elif population < 100 * 30000:
            reps = population // 30000
        elif population < 200 * 40000:
            reps = max(100, population // 40000)
        else:
            reps = max(200, population // 50000)

        results.append({"State": state, "Population": population, "Representatives": reps})

    return results

@app.route("/")
def index():
    """Render the homepage with results."""
    results = get_results()
    return render_template("index.html", results=results)

@app.route("/download")
def download_csv():
    """Generate and serve CSV file."""
    results = get_results()
    df = pd.DataFrame(results)

    # Create CSV response
    csv_data = df.to_csv(index=False)
    response = Response(csv_data, mimetype="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=madison_representation.csv"
    return response

@app.route("/download-json")
def download_json():
    results = get_results()
    # Convert the results to a JSON string
    json_data = json.dumps(results, indent=2)
    response = make_response(json_data)
    response.mimetype = 'application/json'
    response.headers["Content-Disposition"] = "attachment; filename=madison_representation.json"
    return response

@app.route("/download-pdf")
def download_pdf():
    results = get_results()
    rendered = render_template("printable.html", results=results)  # Create a print-friendly template
    pdf = weasyprint.HTML(string=rendered).write_pdf()
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=madison_representation.pdf"
    return response

@app.route("/download-excel")
def download_excel():
    """Generate and serve Excel file."""
    results = get_results()
    df = pd.DataFrame(results)

    # Create an in-memory Excel file
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Representation")

    output.seek(0)

    response = Response(output.getvalue(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response.headers["Content-Disposition"] = "attachment; filename=madison_representation.xlsx"
    return response

if __name__ == "__main__":
    app.run()