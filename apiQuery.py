import requests

# Replace with your API key and SightMap endpoint
API_KEY = "dstNUzcI29uBYBBxwogzs2u4dy7mWu24"
BASE_URL = "https://api.sightmap.com/v1/assets"
UNIT_URL = "/multifamily/units"
EXPENSE_URL = "/multifamily/expenses"

# Set up headers for authentication
headers = {
    "API-Key": API_KEY,
    "Content-Type": "application/json",
    "Experimental-Flags": "expenses"
}

def get_sightmap_data():
    print("Attempting API Connection...")
    try:
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)

        data = response.json()
        data = data['data']

        if isinstance(data, list):
            assetID = [f"/{item['id']}" for item in data if 'id' in item]
        elif isinstance(data, dict) and 'id' in data:
            assetID = [f"/{data['id']}"]
        else:
            assetID = "Failure \n"

        response = requests.get(BASE_URL + assetID[0] + UNIT_URL, headers=headers)
        response.raise_for_status()

        nextURL = UNIT_URL
        firstPass = True

        while nextURL:
            if firstPass:
                data = response.json()
                nextURL = data["paging"]
                nextURL = nextURL["next_url"]
                unitData = data['data']
                firstPass = False
            else:
                response = requests.get(nextURL, headers=headers)
                response.raise_for_status()
                data = response.json()
                nextURL = data["paging"]
                nextURL = nextURL["next_url"]
                unitData.extend(data['data'])

        response = requests.get(BASE_URL + assetID[0] + EXPENSE_URL, headers=headers)

        expenseData = response.json()
        expenseData = expenseData["data"]

        sendback = {"units" : unitData, "expenses" : expenseData}
        print("\nAPI connection complete!")
        return sendback
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
