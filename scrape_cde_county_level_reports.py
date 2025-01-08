import csv
import requests
import pathlib

# read the state and county level reports from the CDE website
# and save them to a local directory
# 1. First, read the FIPS codes TSV file from US_FIPS_Codes.tsv. yield
#  Alabama	Autauga	01	001


def read_fips_codes():
    # yield each row in the file
    with open("US_FIPS_Codes.tsv") as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            yield row


# https://eji.cdc.gov/documents/data/2024/countymaps/26_Michigan/26077_Kalamazoo_County_Michigan.pdf
def generate_url_path(state_fips, state, county_fips, county):
    return f"documents/data/2024/countymaps/{state_fips}_{state}/{state_fips}{county_fips}_{county}_County_{state}.pdf"


def generate_url(path):
    return f"https://eji.cdc.gov/{path}"


def download(url, path):
    print("Downloading", url, "to", path)
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to download", url)
        return
    # ensure the directory exists
    parent = pathlib.Path(path).parent
    pathlib.Path(parent).mkdir(parents=True, exist_ok=True)

    with open(path, "wb") as file:
        file.write(response.content)


if __name__ == "__main__":
    print("Scraping CDE County Level Reports")
    fips_codes = read_fips_codes()
    for index, row in enumerate(fips_codes):
        print(f"Processing row {index + 1} with {row}")
        state, county, state_fips, county_fips = row
        path = generate_url_path(state_fips, state, county_fips, county)
        # check if file exists
        if pathlib.Path(path).exists():
            print("File exists", path)
            continue
        url = generate_url(path)
        print("URL", url)
        download(url, path)
