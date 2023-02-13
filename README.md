
# Lottery System API


This project is a REST API built using Python3 and the Flask web framework. It provides a simulation of a lottery system, allowing users to place multiple bets at once through POST requests and view the history of previous bets through GET requests. Additionally, users are able to specify a specific time period when retrieving the history of placed bets. The API makes use of the powerful data manipulation capabilities of the Pandas library to handle and save new bets, as well as to retrieve and filter historical placed bets. The bets placed through the API are saved as CSV files, providing a convenient and accessible means of storing and retrieving data. This API offers a user-friendly, flexible, and efficient solution for those looking to implement a lottery system, making it easy to place bets, retrieve information about past betting activity, and manage the underlying data.


## Authors

- [@Nils Elvefors](https://github.com/nilselvefors)


## API Reference

#### Place bet

```http
  POST /
```

| Parameter | Type | Required   | Fortmat|                    
| :-------- | :------- | :-------   |:-------|
| `NAME`   | `string` |  **True** |       |
| `NUMBER`   | `int`   |  **True** |        |
| `EMAIL`   | `string`   |  **True** |      |
| `DATE`   | `string`   |  **True** |    yyyy-mm-dd    |
| `TIME`   | `string`   |  **True** |    hh    |

#### Get historical data

```http
  GET /
```

| Parameter | Type     | Required   | Info |                    
| :-------- | :------- | :-------   |:-------|
| `start`   | `string` |  **False** |  Used in combination with end-parameter      |
| `end`   | `string`   |  **False** |   Used in combination with start-parameter        |


## Installation

#### Install requirements
```bash
pip install -r Lottery-System-using-API/requirements.txt
```

#### Start server
```bash
python3 Lottery-System-using-API/API.py 
```
## Making requests to server

#### Place single bet

```python
import requests

# declaring URL
URL = ""

# declaring parameters
PARAMS = {
    NAME: "Nils Elvefors",
    NUMBER: 100,
    EMAIL: "my@email.com",
    DATE: "2023-05-10",
    TIME: "13"
}

# sending request
response = requests.post(url = URL, params = PARAMS)
  
# extracting data in json format
data = response.json()
```


#### Place multiple bets

```python
import requests

# declaring URL
URL = ""

# declaring parameters
PARAMS = {
    NAME: "Nils Elvefors",
    NUMBER: [100,10,35,22],
    EMAIL: "my@email.com",
    DATE: ["2023-05-10","2023-01-18","2023-01-18","2023-02-18"],
    TIME: ["13","03","21","00"]
}

# sending request
response = requests.post(url = URL, params = PARAMS)
  
# extracting data in json format
data = response.json()
```


#### Retrieve all placed bets

```python
import requests

# declaring URL
URL = ""

# sending request
response = requests.get(url = URL)
  
# extracting data in json format
data = response.json()
```

#### Retrieve bets placed in specific time period 

```python
import requests

# declaring URL
URL = ""

# declaring parameters
PARAMS = {
    start: "2010-12-01",
    end: "2011-05-01",
}

# sending request
response = requests.get(url = URL, params = PARAMS)
  
# extracting data in json format
data = response.json()
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

