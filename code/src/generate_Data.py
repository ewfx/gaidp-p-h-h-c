from faker import Faker
import random
import csv
from datetime import datetime

fake = Faker()
def generate_fake_data(num_records):
    data = []
    for _ in range(num_records):
        record = {
            "CustomerID": fake.bothify(text="CUST-####-????"),
            "InternalObligorID": fake.random_number(digits=5, fix_len=True),
            "OriginalInternalObligorID": fake.random_number(digits=5, fix_len=True),
            "ObligorName": fake.name(),
            "City": fake.city(),
            "Country": random. choice (["US", "USA"]),
            "ZipCodeForeignMailingCode": fake.zipcode(),
            "IndustryCode": fake.random_int(min=1000, max=999999),
            "IndustryCodeType": random.choice(["1. NAICS", "2. SIC", "3. GICS"]),
            "InternalRating": fake.text(max_nb_chars=50),
            "TIN": random.choice([fake.bothify(text="##-#######"), fake.bothify(text="#######"), "NA", "Invalid"]),
            "StockExchange": random.choice(["NYSE", "OTC", "NASDAQ", "NA"]),
            "TKR": fake.text(max_nb_chars=5),
            "CUSIP": random.choice([fake.bothify(text="######"), "NA"]),
            "InternalCreditFacilityID": fake.bothify(text="######"),
            "OriginalInternalCreditFacilityID": random.choice([fake.bothify(text="###,???"), fake.bothify(text="###")]),
            # Dont use
            "OriginationDate": fake.date(),
            "MaturityDate": fake.date(),
            "FacilityType": fake.random_int(min=0, max=19),
            "OtherFacilityType": random.choice([fake.text(max_nb_chars=50), "", "NA"]),
            "CreditFacilityPurpose": fake.random_int(min=0, max=19),
            "OtherFacilityPurpose": fake.text(max_nb_chars=50),
            "CommittedExposure": random.choice([fake.random_int(min=10000, max=999999), "NA"]),
            "UtilizedExposure": random. choice([fake.random_int(min=10000, max=999999), "NA"]),
            "LineReportedOnFRY9C": random. choice([fake.random_int(min=1, max=11), "NA"]),
            "LineOfBusiness": fake.text(max_nb_chars=50),
            "CumulativeChargeoffs": random.choice([fake.random_int(min=10000, max=999999), "NA", "0", "Invalid"]),
            "PastDue": random.choice([fake.random_int(min=0, max=60), "NA"]),
            "NonAccrualDate": random.choice([fake.date(), "NA"]),
            "ParticipationFlag": random.choice(["NA", 1, 2, 3, 4, 5])
        }
        data.append(record)
    return data

def save_to_csv(data, filename):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    num_records = 100
    fake_data = generate_fake_data(num_records)
    save_to_csv(fake_data, "fake_data.csv")
    print("Data saved successfully")