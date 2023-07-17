from src.requestDataFromEach import requestDataFromEach;
from src.grabTop100 import getTop100;
from src.countUniqueColours import countUniqueColours;
import os;

# create a list of countries to iterate through
countries = ["jp"];
# countries = ["jp", "gb", "us", "cn", "kr"];
# common countries: us, cn, kr, gb, jp


# create a folder for the country if it doesn't exist
if not os.path.exists("data"): os.mkdir("data");

# getTop100(countries);
requestDataFromEach(countries);
countUniqueColours(countries);