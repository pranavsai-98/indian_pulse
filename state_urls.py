import json
india_news_urls = {
    "Andhra Pradesh": "https://timesofindia.indiatimes.com/india/andhra-pradesh",
    "Arunachal Pradesh": "https://timesofindia.indiatimes.com/india/arunachal-pradesh",
    "Assam": "https://timesofindia.indiatimes.com/india/assam",
    "Bihar": "https://timesofindia.indiatimes.com/india/bihar",
    "Chhattisgarh": "https://timesofindia.indiatimes.com/india/chhattisgarh",
    "Goa": "https://timesofindia.indiatimes.com/india/goa",
    "Gujarat": "https://timesofindia.indiatimes.com/india/gujarat",
    "Haryana": "https://timesofindia.indiatimes.com/india/haryana",
    "Himachal Pradesh": "https://timesofindia.indiatimes.com/india/himachal-pradesh",
    "Jharkhand": "https://timesofindia.indiatimes.com/india/jharkhand",
    "Karnataka": "https://timesofindia.indiatimes.com/india/karnataka",
    "Kerala": "https://timesofindia.indiatimes.com/india/kerala",
    "Madhya Pradesh": "https://timesofindia.indiatimes.com/india/madhya-pradesh",
    "Maharashtra": "https://timesofindia.indiatimes.com/india/maharashtra",
    "Manipur": "https://timesofindia.indiatimes.com/india/manipur",
    "Meghalaya": "https://timesofindia.indiatimes.com/india/meghalaya",
    "Mizoram": "https://timesofindia.indiatimes.com/india/mizoram",
    "Nagaland": "https://timesofindia.indiatimes.com/india/nagaland",
    "orissa": "https://timesofindia.indiatimes.com/india/orissa",
    "Punjab": "https://timesofindia.indiatimes.com/india/punjab",
    "Rajasthan": "https://timesofindia.indiatimes.com/india/rajasthan",
    "Sikkim": "https://timesofindia.indiatimes.com/india/sikkim",
    "Tamil Nadu": "https://timesofindia.indiatimes.com/india/tamil-nadu",
    "Telangana": "https://timesofindia.indiatimes.com/india/telangana",
    "Tripura": "https://timesofindia.indiatimes.com/india/tripura",
    "Uttar Pradesh": "https://timesofindia.indiatimes.com/india/uttar-pradesh",
    "Uttarakhand": "https://timesofindia.indiatimes.com/india/uttarakhand",
    "West Bengal": "https://timesofindia.indiatimes.com/india/west-bengal",

    # Union Territories
    "Andaman and Nicobar Islands": "https://timesofindia.indiatimes.com/india/andaman-and-nicobar-islands",
    "Chandigarh": "https://timesofindia.indiatimes.com/india/chandigarh",
    "Dadra and Nagar Haveli": "https://timesofindia.indiatimes.com/india/dadra-and-nagar-haveli",
    "Delhi": "https://timesofindia.indiatimes.com/india/delhi",
    "Jammu and Kashmir": "https://timesofindia.indiatimes.com/india/jammu-and-kashmir",
    "Lakshadweep": "https://timesofindia.indiatimes.com/india/lakshadweep",
}


with open('india_news_urls.json', 'w') as f:
    json.dump(india_news_urls, f, indent=4)
