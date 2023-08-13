from src.requestDataFromEach import requestDataFromEach;
from src.grabTop100 import getTop100;
from src.countUniqueColours import countUniqueColours;
from src.assessImages import assessImages;
import os;

# create a list of countries to iterate through
countries = ["jp", "gb"];
# common countries: us, cn, kr, gb, jp

# create a folder for the country if it doesn't exist
if not os.path.exists("data"): os.mkdir("data");

# call the functions
getTop100(countries);
requestDataFromEach(countries);
countUniqueColours(countries);
assessImages();