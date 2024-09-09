# Exchange Rate Fetcher

Overview

This is a Python command-line utility that fetches the exchange rates for EUR and USD from PrivatBank's public API for the last few days (up to 10 days). The program is designed to retrieve both the sale and purchase rates for these currencies on specified dates.

Features

Fetches exchange rates (both sale and purchase) for EUR and USD from PrivatBank for the last specified days.

Can retrieve exchange rates for up to 10 days.

Asynchronous HTTP requests using the aiohttp library for efficient network communication.

Handles network errors gracefully and ensures robust data retrieval.

Implements principles of SOLID for maintainable and scalable code.

Usage

Clone the repository.

Install the dependencies using pip:

pip install aiohttp

Run the script from the command line, specifying the number of days (up to 10) for which you want to fetch the exchange rates:

python main.py <days>

Example:

python main.py 2

The program will output the exchange rates in the following format:

[
  {
    "03.11.2022": {
      "EUR": {
        "sale": 39.4,
        "purchase": 38.4
      },
      "USD": {
        "sale": 39.9,
        "purchase": 39.4
      }
    }
  },
  {
    "02.11.2022": {
      "EUR": {
        "sale": 39.4,
        "purchase": 38.4
      },
      "USD": {
        "sale": 39.9,
        "purchase": 39.4
      }
    }
  }
]

Restrictions

The program supports fetching exchange rates for up to 10 days. If you specify more than 10 days, an error will be raised.

Dependencies

Python 3.7+
aiohttp
