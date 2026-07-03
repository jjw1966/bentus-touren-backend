from flask import Flask, jsonify
from data.drive_connector import download_excel_from_drive
from data.excel_reader import read_excel_data

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    file_path = download_excel_from_drive()
    data = read_excel_data(file_path)
    return jsonify(data)

    @app.route("/tourstallning")
    def tourstallning():
                file_path = download_excel_from_drive()
                data = read_excel_data(file_path)
    return jsonify(data.get("tourstallning", {}))

    @app.route("/spelare")
    def spelare():
                            file_path = download_excel_from_drive()
                            data = read_excel_data(file_path)
                            return jsonify(data.get("spelare", {}))

                            @app.route("/lagspel")
                            def lagspel():
                                        file_path = download_excel_from_drive()
                                        data = read_excel_data(file_path)
                                        return jsonify(data.get("lagspel", {}))

                                        if __name__ == "__main__":
                                                    app.run(host="0.0.0.0", port=10000)