# Hello <span style="color:#ff6116">Bitly</span>
## Welcome to my App's docs

---

### Problem
* For a user's default group, gather all the Bitlinks, then fetch the clicks by country within the last 30 days, aggregate the data calculating the average days as clicks/30, and return the result via an HTTP API endpoint<sup>1</sup>

### Assumptions:
* You have some knowledge of
  * Python
  * Linux/macOS
* Your computer runs Linux/macOS
* Your computer is connected to the internet
* You have a Bitly Access Token
  * To make use of our API, you will need a Bitly Access Token
    1. Sign up for a Bitly account if you do not already have one
    2. Visit [this page](https://bitly.is/accesstoken) to get your Access Token.
* You have python v3.8+ installed
  * To check run the following, and verify
```commandline
python3 --version
```

### Requirements
* [x] Tests
* [x] Runs
* [x] Docs
* [x] **FUN!**

### Major Design Decisions
* Python
  * Because it was the most likely to run on the evaluator's computer without long setup instructions
* Flask Framework
  * Easier to set up & use than Django
  * Won't need Django's admin/advanced features for this project
* Security
  * HTTPS was *not* called for
  * Storing the Bitly API Token in an environment variable
    * Minimized the risk of leaking it via a file
 

### Dependencies
* flask
* pandas
* unittest
* others<sup>2</sup>

---
### Setup
Run the following commands from the terminal
#### Create a virtual environment 
```commandline
python3 -m venv venv
```
#### Activate the virtual environment
```commandline
source venv/bin/activate
```
#### Install required packages
```commandline
pip install -r requirements.txt
```
#### Set environment variable(s) 
##### Bitly API Token
```commandline
export BITLY_API_TOKEN=<Your token here>
```

---

### Test
#### Run the following command from the terminal
```commandline
python3 -m unittest
```

---

### Execute
1. Run the following commands from the terminal
```commandline
flask run
```
2. Click on the link displayed in the terminal
   * A new tab will open in your browser
   * Usually the URL will be [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
3. Click the link provided on the landing page to navigate to the API endpoint
   * Usually the URL will be [http://127.0.0.1:5000/api/v1/avgDailyClicksByCountry](http://127.0.0.1:5000/api/v1/avgDailyClicksByCountry) 
4. Switch back to the terminal and press CTRL+C to quit

### Optional
#### Refreshing the test data
* Fake data was provided for testing 
* You can generate new test data with the provided [refresh_test_data.py](refresh_test_data.py) utility
  * It uses a spy pattern to collect actual requests & responses
* If you have not done so already, run the setup steps shown above
* Then, run the commands below
```commandline
python3 refresh_test_data.py
```

---

### Footnotes
1. Source https://git.io/JD5S7
2. Full list can be found in the [requirements.txt](requirements.txt) file
