import requests

URL = "http://localhost:8000/alerts"

# with open("C:\\Users\\shtei\\Desktop\\Joys_Hafifa\\Hafifa\\rolling_exercise\\air_quality_files\\air_quality_2024_11_24.csv", "rb") as f:
#     response = requests.post(
#         URL,
#         files={"file": f}
#     )

response = requests.get(URL)
print(response.status_code)
print(response.text)