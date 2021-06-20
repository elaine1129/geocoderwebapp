from flask import Flask, render_template, request, send_file
from geopy.geocoders import ArcGIS
import pandas
import datetime  # for unique filename

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/success-table', methods=['POST'])
def success_table():
    global filename  # make global to access in the download function
    if request.method == "POST":
        file = request.files['file']
        try:
            # if is mp4 file with .csv extention, then here will have error
            df = pandas.read_csv(file)
            gc = ArcGIS(timeout=3000)
            df['coordinates'] = df['Address'].apply(gc.geocode)

            df['Latitude'] = df['coordinates'].apply(
                lambda x: x.latitude if x != None else None)
            df['Longitude'] = df['coordinates'].apply(
                lambda x: x.longitude if x != None else None)

            df = df.drop("coordinates", 1)
            # if two user submit the data at the same time, this geocoded.csv will have name clash when creating
           # df.to_csv("uploads/geocoded.csv", index=None)  # index
            filename = datetime.datetime.now().strftime(
                "uploads/%Y-%m-%d-%H-%M-%S-%f" + ".csv")
            df.to_csv(filename, index=None)
        # return index.html template
            # return download button
            return render_template("index.html", text=df.to_html(), btn='download.html')
        except:
            return render_template("index.html", text="Please make sure you ave an address column in your CSV file!")


@app.route("/download-file/")
def download():
    # send the file that was generated to the user under the name
    return send_file(filename, attachment_filename='yourfile.csv', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
