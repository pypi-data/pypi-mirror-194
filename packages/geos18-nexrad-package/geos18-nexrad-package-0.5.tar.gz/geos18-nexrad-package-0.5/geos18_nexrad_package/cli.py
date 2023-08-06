import typer
import boto3
import datetime
import calendar
import os
from typing import List
from dotenv import load_dotenv
import time
import botocore.exceptions
from io import BytesIO

load_dotenv()

app = typer.Typer()

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_LOG_ACCESS_KEY = os.environ.get("AWS_LOG_ACCESS_KEY")
AWS_LOG_SECRET_KEY = os.environ.get("AWS_LOG_SECRET_KEY")

dest_bucket_name = "damg7245-noaa-assignment"

s3_client = boto3.client(
    "s3",
    region_name="us-east-1",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
)

s3_client_logs = boto3.client(
    "logs",
    region_name="us-east-1",
    aws_access_key_id=AWS_LOG_ACCESS_KEY,
    aws_secret_access_key=AWS_LOG_SECRET_KEY,
)

def search_file_goes(file_name, s3_client):
    file_name = get_link_goes(file_name)
    try:
        s3_client.head_object(Bucket="noaa-goes18", Key=file_name)
        return True
    except:
        return False

def get_link_goes(file_name):
    parts = file_name.split("_")
    name = "-".join(parts[1].split("-")[:3])
    if name[-1].isdigit():
        name = name[: len(name) - 1]
    year = parts[3][1:5]
    day_of_year = parts[3][5:8]
    hour = parts[3][8:10]
    url = f"ABI-L1b-RadC/{year}/{day_of_year}/{hour}/{file_name}"
    return url

def get_link_nexrad(file_name):
    parts = file_name.split("_")
    station = parts[0][0:4]
    year = parts[0][4:8]
    month = parts[0][8:10]
    day = parts[0][10:12]
    url = f"{year}/{month}/{day}/{station}/{file_name}"
    return url

def get_object_url(bucket_name, object_key, s3_client):
    return s3_client.generate_presigned_url(
        ClientMethod="get_object", Params={"Bucket": bucket_name, "Key": object_key}
    )

def search_file_nexrad(file_name, s3_client):
    file_name = get_link_nexrad(file_name)
    try:
        s3_client.head_object(Bucket="noaa-nexrad-level2", Key=file_name)
        return True
    except:
        return False
    

def download_and_upload_s3_file(
    src_bucket,
    src_object,
    dest_bucket,
    dest_folder,
    dest_object,
    s3_client,
    s3_client_logs,
):
    dest_path = dest_folder + "/" + dest_object
    
    # Check if file already exists in destination bucket
    try:
        s3_client.head_object(Bucket=dest_bucket, Key=dest_path)
        s3_object_url = get_object_url(dest_bucket, dest_path, s3_client).split("?")[0]
        print(f"File already exists in destination bucket. URL: {s3_object_url}")
        return s3_object_url
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            pass
        else:
            raise

    # Read the S3 object as a bytes object
    write_logs(f"Downloading {src_object} from {src_bucket}", s3_client_logs)
    s3_object = s3_client.get_object(Bucket=src_bucket, Key=src_object)
    file_content = s3_object["Body"].read()
    file_obj = BytesIO(file_content)
    write_logs("Downloading completed", s3_client_logs)
    write_logs(
        f"Uploading {src_object} from {src_bucket} to {dest_bucket} under {dest_folder}",
        s3_client_logs,
    )
    
    # Upload the bytes object to another S3 bucket
    s3_client.upload_fileobj(file_obj, dest_bucket, dest_path)
    write_logs(f"Uploading completed", s3_client_logs)
    
    # Get URL to the uploaded file
    s3_object_url = get_object_url(dest_bucket, dest_path, s3_client).split("?")[0]
    print(f"File downloaded successfully. URL: {s3_object_url}")
    
    return s3_object_url



def write_logs(message: str, s3_client_logs):
    s3_client_logs.put_log_events(
        logGroupName="damg7245-noaa-assignment",
        logStreamName="app-logs",
        logEvents=[
            {
                "timestamp": int(time.time() * 1e3),
                "message": message,
            }
        ],
    )


@app.command("create user")
def create_user(username: str):
    """
    Create a new user with the specified username.
    """
    # Code to create user goes here
    typer.echo(f"User {username} created successfully.")

@app.command("download")
def download_file(file_name: str):
    """
    Download the file with the specified name and return its S3 URL.
    """
    # Check if file exists in public bucket
    if file_name.endswith(".nc"):
        if search_file_goes(file_name, s3_client):
            # Download the file and upload it to S3 bucket
            s3_object_url = download_and_upload_s3_file(
                "noaa-goes18",
                get_link_goes(file_name),
                dest_bucket_name,
                "goes",
                file_name,
                s3_client,
                s3_client_logs,
            )
        else:
            typer.echo("File not found in the bucket. Please enter the correct file name.")
    else:
        if search_file_nexrad(file_name, s3_client):
            # Download the file and upload it to S3 bucket
            s3_object_url = download_and_upload_s3_file(
                "noaa-nexrad-level2",
                get_link_nexrad(file_name),
                dest_bucket_name,
                "nexrad",
                file_name,
                s3_client,
                s3_client_logs,
            )  
        else:
            typer.echo("File not found in the bucket. Please enter the correct file name.")

@app.command("fetch")
def list_files(
    datatype: str = typer.Argument(..., help="Data type ('geos18' or 'nexrad')"),
    year: str = typer.Option(..., help="Year"),
    day: str = typer.Option(..., help="Day"),
    hour: str = typer.Option(None, help="hour (only for 'geos18' data type)"),
    month: str = typer.Option(None, help="Month (only for 'nexrad' data type)"),
    station: str = typer.Option(None, help="Station code (only for 'nexrad' data type)"),
):
    """
    List all files in a specified prefix.
    """
    if datatype.lower() == "geos18":
        prefix = f"ABI-L1b-RadC/{year}/{day}/{hour}/"
        bucket = "noaa-goes18"
        result = s3_client.list_objects(Bucket=bucket, Prefix=prefix)
        if not result.get("Contents"):
            typer.echo("No data available.")
        else:
            files = [content["Key"].split("/")[-1] for content in result.get("Contents", [])]
            for file in files:
                typer.echo(file)
    elif datatype.lower() == "nexrad":
        prefix = f"{year}/{month}/{day}/{station}/"
        bucket = "noaa-nexrad-level2"
        result = s3_client.list_objects(Bucket=bucket, Prefix=prefix)
        if not result.get("Contents"):
            typer.echo("No data available. Make ")
        else:
            files = [content["Key"].split("/")[-1] for content in result.get("Contents", [])]
            for file in files:
                typer.echo(file)
    else:
        typer.echo("Invalid data type. Use 'geos18' or 'nexrad'.")


@app.command("fetchall")
def list_files(
    datatype: str = typer.Argument(..., help="Data type ('geos18' or 'nexrad')"),
):
    """
    List all files in a specified prefix.
    """
    if datatype.lower() == "geos18":
        valid_years =["2022", "2023"]
        year = None
        while year not in valid_years:
            year = typer.prompt("Enter year(YYYY)")
            if year=="2022":
                valid_days = ["{:03d}".format(i) for i in range(209, 366)]
                day = typer.prompt("Enter day of year (DDD)")
                while day not in valid_days:
                    typer.echo(f"No data available for the day {day} of year {year}.")
                    day = typer.prompt("Enter day of year (DDD)")
                valid_hours = ["{:02d}".format(i) for i in range(00, 24)]
                hour = typer.prompt("Enter hour(HH)")
                while hour not in valid_hours:
                    typer.echo(f"No data available for the hour {hour} of the day {day} of year {year}. Hour must be between 00 and 23")
                    hour = typer.prompt("Enter hour(HH)")
            if year not in valid_years:
                typer.echo(f"No data available for the year {year}. ABI-L1b-RadC has only two years of data: 2022 and 2023...")
            elif year == "2023":
                now = datetime.datetime.now()
                if now.time() < datetime.time(19, 30):
                    valid_days = ["{:03d}".format(i) for i in range(1, now.timetuple().tm_yday + 1)]
                else:
                    valid_days = ["{:03d}".format(i) for i in range(1, now.timetuple().tm_yday + 2)]
                day = typer.prompt("Enter day of year (DDD)")
                while day not in valid_days:
                    typer.echo(f"No data available for the day {day} of year {year}.")
                    day = typer.prompt("Enter day of year (DDD)")
                valid_hours = ["{:02d}".format(i) for i in range(00, 24)]
                hour = typer.prompt("Enter hour(HH)")
                while hour not in valid_hours:
                    typer.echo(f"No data available for the hour {hour} of the day {day} in year {year}. Hour must be between 00 and 23")
                    hour = typer.prompt("Enter hour(HH)")
        typer.echo("\n")            
        prefix = f"ABI-L1b-RadC/{year}/{day}/{hour}/"
        bucket = "noaa-goes18"
        result = s3_client.list_objects(Bucket=bucket, Prefix=prefix)
        if not result.get("Contents"):
            typer.echo("No data available.")
        else:
            typer.echo("THE FILES AVAILABLE IN THE BUCKET ARE:\n")
            files = [content["Key"].split("/")[-1] for content in result.get("Contents", [])]
            for file in files:
                typer.echo(file)
    elif datatype.lower() == "nexrad":
        valid_years = ["1970"] + [str(i) for i in range(1991, 2024)]
        year = typer.prompt("Enter year(YYYY)")        
        while year not in valid_years or len(year)!= 4:
            typer.echo("Invalid year.")
            year = typer.prompt("Enter year(YYYY)")
        month = None
        while not month:
            month = typer.prompt("Enter month(MM)")
            if not month.isdigit() or len(month) != 2 or not 1 <= int(month) <= 12:
                typer.echo("Invalid month. Month must be a number between 01 and 12.")
                month = None
        _, num_days = calendar.monthrange(int(year), int(month))
        valid_days = ["{:02d}".format(day) for day in range(1, num_days + 1)]
        day = None
        while not day:
            day = typer.prompt("Enter day(DD)")
            if not day.isdigit() or day not in valid_days or len(day) != 2:
                typer.echo(f"No data available for day {day} of month {month} in year {year}.")
                day = None
        station = None        
        while not station or not station.isalpha() or len(station) != 4:
            station = typer.prompt("Enter station code(XXXX)")
            if not station.isalpha():
                typer.echo("Invalid station code.")
            elif len(station) != 4:
                typer.echo("Invalid station code.")
        station = station.upper()
        typer.echo("\n")
        prefix = f"{year}/{month}/{day}/{station}/"
        bucket = "noaa-nexrad-level2"
        result = s3_client.list_objects(Bucket=bucket, Prefix=prefix)
        if not result.get("Contents"):
            typer.echo("No data available.")
        else:
            typer.echo("THE FILES AVAILABLE IN THE BUCKET ARE:\n")
            files = [content["Key"].split("/")[-1] for content in result.get("Contents", [])]
            for file in files:
                typer.echo(file)
    else:
        typer.echo("Invalid data type. Use 'geos18' or 'nexrad'.")

@app.command("fetch2")
def list_files(
    datatype: str = typer.Argument(..., help="Data type ('GEOS18')"),
    year: str = typer.Argument(None, help="Year (YYYY)"),
    day: str = typer.Argument(None, help="Day of year (DDD) (for GEOS18)"),
    hour: str = typer.Argument(None, help="Hour (HH) (for GEOS18)"),
):
    """
    List all files in a specified prefix.
    """
    if datatype.upper() == "GEOS18":
        valid_years = ["2022", "2023"]
        if year not in valid_years:
            typer.echo(
                f"Invalid year {year}. ABI-L1b-RadC has only two years of data: 2022 and 2023."
            )
            raise typer.Abort()
        valid_days = [
            "{:03d}".format(i) for i in range(1, 367 if year == "2020" else 366)
        ]
        if day not in valid_days:
            typer.echo(f"Invalid day {day} for year {year}")
            raise typer.Abort()
        valid_hours = ["{:02d}".format(i) for i in range(24)]
        if hour not in valid_hours:
            typer.echo(f"Invalid hour {hour} for year {year} and day {day}")
            raise typer.Abort()
        typer.echo("\n")
        prefix = f"ABI-L1b-RadC/{year}/{day}/{hour}/"
        bucket = "noaa-goes18"
        result = s3_client.list_objects(Bucket=bucket, Prefix=prefix)
        if not result.get("Contents"):
            typer.echo("No data available.")
        else:
            typer.echo("THE FILES AVAILABLE IN THE BUCKET ARE:\n")
            files = [content["Key"].split("/")[-1] for content in result.get("Contents", [])]
            for file in files:
                typer.echo(file)
    else:
        typer.echo("Datatype must be GEOS18")

@app.command("fetch3")
def list_files(
    datatype: str = typer.Argument(..., help="Data type ('NEXRAD')"),
    year: str = typer.Argument(None, help="Year (YYYY)"),
    month: str = typer.Argument(None, help="Month (MM) (for Nexrad)"),
    nexrad_day: str = typer.Argument(None, help="Day (DD) (for Nexrad)"),
    station: str = typer.Argument(None, help="Station code (XXXX) (for Nexrad)"),
):
    """
    List all files in a specified prefix.
    """
    if datatype.upper() == "NEXRAD":
        valid_years = ["1970"] + [str(i) for i in range(1991, 2024)]
        if year not in valid_years:
            typer.echo(
                f"Invalid year {year}. Nexrad data is available for years 1970 and 1991-2023."
            )
            raise typer.Abort()
        valid_months = ["{:02d}".format(i) for i in range(1, 13)]
        if month not in valid_months:
            typer.echo(f"Invalid month {month} for year {year}")
            raise typer.Abort()
        month_num = int(month)
        if nexrad_day is None:
            last_day = (datetime.date(int(year), month_num, 1) + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1)
            nexrad_day = last_day.strftime('%d')
        if not nexrad_day.isdigit() or not 1 <= int(nexrad_day) <= 31:
            typer.echo(f"Invalid day {nexrad_day} for month {month} and year {year}")
            raise typer.Abort()
        valid_stations = ["{:04d}".format(i) for i in range(1000, 10000)]
        if not station or len(station) != 4 or not station.isalpha():
            typer.echo(f"Invalid station code {station}")
            raise typer.Abort()
        prefix = f"{year}/{month}/{nexrad_day}/{station.upper()}/"
        bucket = "noaa-nexrad-level2"
        result = s3_client.list_objects(Bucket=bucket, Prefix=prefix)
        if not result.get("Contents"):
            typer.echo("No data available.")
        else:
            typer.echo("THE FILES AVAILABLE IN THE BUCKET ARE:\n")
            files = [content["Key"].split("/")[-1] for content in result.get("Contents", [])]
            for file in files:
                typer.echo(file)
    else:
        typer.echo("Datatype must be NEXRAD")            


if __name__ == "__main__":
    app()