from googleapiclient.discovery import build



#open key file and read in api key

with open ("key", "r") as myfile:
    api_key=myfile.read()

#opening the google API service using the api-key

with build('youtube', 'v3', developerKey=api_key) as youtube:
    
    request = youtube.search().list(part='snippet', q='music', maxResults=10)

    response = request.execute()

    print(response)