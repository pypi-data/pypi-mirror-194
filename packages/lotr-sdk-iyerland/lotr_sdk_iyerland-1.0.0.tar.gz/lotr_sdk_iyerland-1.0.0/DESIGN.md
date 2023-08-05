# Introduction
The purpose of this SDK is to abstract the `[The One API](`https://the-one-api.dev/)`. It serves your needs regarding data about The Lord of the Rings, the epic books by J. R. R. Tolkien and the official movie adaptions by Peter Jackson.
This SDK limits itself to the following endpoints due to time constraints and will be updated as and when time permits:

- /movie
- /movie/{id}
- /movie/{id}/quote

## Design Principles
The code is fairly straight forward and design is pretty simple due to 
time constraints, as I did not want to add too many features and my main
criteria was to get it to a working state with tests and out of the door.

The structure of the package is intentionally flat as this is the first iteration and 
this could change moving forward by including `common` and `client` packages 
and moving the logging and retries functional in `common`, the `OneApiSdk` itself
could be moved to `client` package with only the REST calls being made there!

Clients can use the methods provided by the SDK to make requests to the One API
and retrieve data in a structured format. The SDK abstracts away many of 
the low-level details of making HTTP requests and parsing JSON responses, 
making it easier and more convenient to work with the One API.

Clients should handle errors appropriately as this SDK can raise exceptions when 
errors occur, and clients should catch and handle these exceptions appropriately. 
For example, clients could log the error and display a user-friendly message to the user.

## How to use this SDK

0. Sign up [here](https://the-one-api.dev/sign-up) and get your access token (API Key).

1. Install the SDK:
   ```
    pip3 install lotr_sdk_iyerland
    pip3 install urllib3 
    
   ```
2. Import the SDK: 
   ```
   # open up a python shell
   import lotr_sdk_iyerland
   from lotr_sdk_iyerland import OneApiSdk
   ```
3. Create an instance of the SDK:
   ```
    api_key = 'your_api_key_here'
    one_api_sdk = OneApiSdk(api_key, log_level=logging.DEBUG)
   ``` 
4. Use the SDK:
   ```
    try:
        # Get all movies
        movies = one_api_sdk.get_movies()

        # Get a specific movie by ID
        movie_id = '5cd95395de30eff6ebccde5c'
        movie = one_api_sdk.get_movie(movie_id)

        # Get quotes for a specific movie
        movie_quotes = one_api_sdk.get_movie_quotes(movie_id)
    except Exception as e:
      print(f'Error: {str(e)}')
   ```

