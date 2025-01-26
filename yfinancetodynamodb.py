import boto3
import yfinance as yf
from decimal import Decimal
import pandas as pd
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# DynamoDB table name
TABLE_NAME = "StockData"

# AWS DynamoDB resource
dynamodb = boto3.resource("dynamodb", region_name="us-west-2")  # Replace with your region
table = dynamodb.Table(TABLE_NAME)

def convert_to_decimal(data):
    """
    Recursively convert all float values in a dictionary or list to Decimal.
    :param data: Input dictionary or list
    :return: Updated dictionary or list
    """
    if isinstance(data, list):
        return [convert_to_decimal(i) for i in data]
    elif isinstance(data, dict):
        return {k: convert_to_decimal(v) for k, v in data.items()}
    elif isinstance(data, float):  # Convert float to Decimal
        return Decimal(str(data))
    return data

def save_to_dynamodb(symbol, data):
    """
    Save historical stock data to DynamoDB.
    :param symbol: Stock symbol
    :param data: Pandas DataFrame of stock data
    """
    with table.batch_writer() as batch:
        for index, row in data.iterrows():
            # Prepare the item with Decimal conversion
            item = {
                "Symbol": symbol,
                "Date": str(index.date()),  # Convert Timestamp to string
                "Open": Decimal(str(row["Open"])) if not pd.isna(row["Open"]) else None,
                "High": Decimal(str(row["High"])) if not pd.isna(row["High"]) else None,
                "Low": Decimal(str(row["Low"])) if not pd.isna(row["Low"]) else None,
                "Close": Decimal(str(row["Close"])) if not pd.isna(row["Close"]) else None,
                "Volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else None,
            }
            item = {k: v for k, v in item.items() if v is not None}  # Remove None values
            batch.put_item(Item=item)
    print(f"Data for {symbol} saved to DynamoDB.")

def fetch_and_save(symbol, period="1mo", interval="1d"):
    """
    Fetch stock data from yfinance and save it to DynamoDB.
    :param symbol: Stock symbol
    :param period: Period of data to fetch (e.g., '1mo', '6mo', '1y', etc.)
    :param interval: Data interval (e.g., '1d', '1wk', '1mo', etc.)
    """
    try:
        # Fetch data from yfinance
        stock = yf.Ticker(symbol)
        data = stock.history(period=period, interval=interval)

        if data.empty:
            print(f"No data found for {symbol}.")
            return

        # Save to DynamoDB
        save_to_dynamodb(symbol, data)

    except NoCredentialsError:
        print("AWS credentials not found.")
    except PartialCredentialsError:
        print("Incomplete AWS credentials.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example symbols
    symbols = ["AAPL", "MSFT", "GOOGL"]  # Add your stock symbols here
    for symbol in symbols:
        fetch_and_save(symbol, period="1mo", interval="1d")
