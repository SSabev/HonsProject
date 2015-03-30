library(ggplot2)
library(reshape)
library(scales)

setwd('Dev/HonsProject/Work/Rscripts')


# destinations = c('Aarhus', 'Abbotsford', 'Aberdeen', 'Abha', 'Abidjan', 'Abilene', 'Abu Dhabi',
#                   'Abu Simbel', 'Abuja', 'Acapulco', 'Accra', 'Adana', 'Addis Ababa', 'Adelaide', 'Aden',
#                   'Afghanistan', 'Agadir', 'Agen', 'Agra', 'Agri', 'Ahmedabad', 'Airlie Beach', 
#                   'Ajaccio', 'Akron', 'Al Ain', 'Albania', 'Albany', 'Albert', 'Albuquerque',
#                   'Albury', 'Alderney', 'Aleppo', 'Alexandria', 'Algeria', 'Algiers', 'Alicante',
#                   'Alice Springs', 'Allentown', 'Alliance', 'Almaty', 'Almeria', 'Alor Setar', 
#                   'Alta', 'Amarillo', 'Ambon', 'Amman', 'Amritsar', 'Amsterdam', 'Anaa', 'Anchorage',
#                   'Ancona', 'Angeles', 'Angers', 'Anglesey', 'Angola', 'Anguilla', 'Ankara', 'Annaba', 
#                   'Antalya', 'Antofagasta', 'Antwerp', 'Aomori', 'Apia', 'Appleton',
#                   'Arequipa', 'Argentina', 'Armenia', 'Armidale', 'Arua', 'Aruba', 'Arusha', 'Asheville',
#                   'Ashland', 'Asmara', 'Aspen', 'Astana', 'Astrakhan', 'Asturias', 'Asuncion',
#                   'Athens', 'Atlanta', 'Atlantic City', 'Atyrau', 'Auckland', 'Augsburg', 'Augusta', 
#                  'Austin', 'Australia', 'Austria', 'Avignon', 'Ayers Rock', 'Azerbaijan',
#                  'Baghdad', 'Bahamas', 'Bahrain', 'Baise', 'Bakersfield', 'Baku', 'Balikpapan',
#                  'Ballina', 'Baltimore', 'Bamako', 'Banda Aceh', 'Bangalore', 'Bangkok', 
#                  'Bangladesh', 'Bangor', 'Bangui', 'Barbados', 'Barcelona', 'Bari', 'Barra',
#                  'Barranquilla', 'Barrow', 'Basco', 'Basel', 'Basra', 'Bata', 'Bathurst',
#                  'Batman', 'Baton Rouge', 'Beaumont', 'Beckley', 'Beijing', 'Beirut', 
#                  'Bejaia', 'Belarus', 'Belfast', 'Belgium', 'Belgorod', 'Belgrade',
#                  'Belize City', 'Belize', 'Bellingham', 'Belo Horizonte', 'Bemidji', 
#                  'Benghazi', 'Benin City', 'Benin', 'Bergen', 'Berlin', 'Bermuda',
#                  'Bern', 'Bethel', 'Bhavnagar', 'Bhopal', 'Bhubaneswar', 'Bhuj', 'Bhutan',
#                  'Biarritz', 'Bilbao', 'Billings', 'Bimini', 'Binghamton', 'Birdsville',
#                  'Birmingham', 'Bismarck', 'Blackpool', 'Blantyre', 'Blenheim', 'Bloemfontein', 
#                  'Bloomington', 'Bodo', 'Bodrum', 'Bogota', 'Boise', 'Bol', 'Bolivia', 'Bologna',
#                  'Bolzano', 'Bonaire', 'Bonito', 'Bora Bora', 'Bordeaux', 'Boston', 'Botswana', 
#                  'Bournemouth', 'Bozeman', 'Bradford', 'Brasilia', 'Bratislava', 'Brazil', 
#                  'Brazzaville', 'Bremen', 'Brest', 'Bridgetown', 'Brisbane', 'Bristol', 'Brno', 
#                  'Broken Hill', 'Broome', 'Brownsville', 'Brunei', 'Brunswick', 'Brussels', 
#                  'Bucharest', 'Budapest', 'Buenos Aires', 'Buffalo', 'Bulawayo', 'Bulgaria',
#                  'Bundaberg', 'Burbank', 'Burgos', 'Burkina Faso', 'Burlington', 'Burnie', 'Bursa',
#                  'Burundi', 'Busan', 'Butte', 'Ca Mau', 'Caen', 'Cagayan De Oro', 'Cagliari',
#                  'Cairns', 'Cairo', 'Calabar', 'Calgary', 'Cali', 'Calvi', 'Cambodia', 'Cambridge',
#                  'Cameroon', 'Campbell River', 'Campbeltown', 'Canada', 'Canberra', 'Cancun', 
#                  'Cannes', 'Cape Girardeau', 'Cape Town', 'Caracas', 'Carcassonne', 'Cardiff', 
#                  'Carlsbad', 'Carmel', 'Cartagena', 'Casablanca', 'Casper', 'Castlegar',
#                  'Castletown', 'Catania', 'Cayenne', 'Cayo Coco', 'Cebu', 'Cedar City', 
#                  'Cedar Rapids', 'Ceduna', 'Chad', 'Champaign', 'Chandigarh', 'Changsha', 
#                  'Charleston', 'Charlotte', 'Charlottesville', 'Charlottetown', 'Chattanooga', 
#                  'Chelyabinsk', 'Chengdu', 'Chennai', 'Cheongju', 'Chester', 'Cheyenne', 
#                  'Chiang Mai', 'Chiang Rai', 'Chicago', 'Chihuahua', 'Chile', 'China', 'Chios', 'Chita', 
#                  'Chittagong', 'Chongqing', 'Christchurch', 'Christmas Island', 'Churchill', 'Cincinnati',
#                  'Clearwater', 'Cleveland', 'Clovis', 'Coca', 'Coffs Harbour', 'Coimbatore', 'College Station',
#                  'Cologne', 'Colombia', 'Colombo', 'Colorado Springs', 'Columbia', 'Columbus', 'Comox', 
#                  'Concepcion', 'Congo', 'Constantine', 'Copenhagen', 'Cordoba', 'Cordova', 'Corfu', 'Cork', 
#                  'Corpus Christi', 'Costa Rica', 'Cotabato', 'Cotonou', 'Cozumel', 'Craiova', 'Cranbrook', 
#                  'Crescent City', 'Crete', 'Croatia', 'Crooked Creek', 'Cuba', 'Cuiaba', 'Curacao', 'Curitiba', 
#                  'Cuzco', 'Cyprus', 'Czech Republic', 'Da Nang', 'Daegu', 'Dakar', 'Dalian', 'Dallas', 'Damascus',
#                  'Dammam', 'Dar Es Salaam', 'Darwin', 'Davao', 'Dawson Creek', 'Dayton', 'Daytona Beach',
#                  'Deer Lake', 'Dehra Dun', 'Del Rio', 'Delhi', 'Denmark', 'Denver', 'Derby', 'Derry', 
#                  'Des Moines', 'Detroit', 'Devonport', 'Dhaka', 'Dickinson', 'Dijon', 'Dili', 'Diyarbakir', 
#                  'Djibouti', 'Dodge City', 'Doha', 'Dominica', 'Dominican Republic', 'Doncaster', 'Donegal', 
#                  'Donetsk', 'Dortmund', 'Dothan', 'Dresden', 'Dubai', 'Dubbo', 'Dublin', 'Dubrovnik', 'Duluth',
#                  'Dundee', 'Dunedin', 'Durango', 'Durban', 'Durham', 'Dusseldorf', 'East London', 'Easter Island', 
#                  'Eau Claire', 'Ecuador', 'Edinburgh', 'Edmonton', 'Egypt', 'Eindhoven', 'Ekaterinburg', 
#                  'El Nido', 'El Paso', 'Eldoret', 'Elko', 'Elmira', 'Ende', 'Entebbe', 'Enugu', 
#                  'Equatorial Guinea', 'Erbil', 'Erie', 'Eritrea', 'Eskisehir', 'Esperance', 'Estonia', 
#                  'Ethiopia', 'Eugene', 'Evansville', 'Exeter', 'Fairbanks', 'Faisalabad', 'Fak Fak', 
#                  'Falkland Islands', 'Fall River', 'Fargo', 'Farmington', 'Faro', 'Faroe Islands', 
#                  'Fayetteville', 'Fes', 'Fiji', 'Finland', 'Flint', 'Florence', 'Florencia', 'Flores', 
#                  'Florianopolis', 'Forde', 'Fort Lauderdale', 'Fort Mcmurray', 'Fort Myers', 'Fort Smith', 
#                  'Fort Wayne', 'Fortaleza', 
#                  'France', 'Frankfurt', 'Franklin', 'Fredericton', 'Freeport', 'Freetown', 'French Guiana',
#                  'French Polynesia', 'Fresno', 'Fuerteventura', 'Fukuoka', 'Fukushima', 'Gabon', 'Gaborone', 
#                  'Gainesville', 'Galapagos Is', 'Galena', 'Gambia', 'Gan Island', 'Gander', 'Gaziantep', 
#                  'Gdansk', 'General Santos', 'Geneva', 'Genoa', 'George Town', 'George', 'Georgetown', 'Georgia',
#                  'Geraldton', 'Germany', 'Ghana', 'Gibraltar', 'Gisborne', 'Gladstone', 'Glasgow', 'Gloucester', 
#                  'Goa', 'Goiania', 'Gold Coast', 'Gorakhpur', 'Gothenburg', 'Gran Canaria', 'Granada', 
#                  'Grand Canyon', 'Grand Cayman Island', 'Grand Forks', 'Grand Island', 'Grand Junction', 
#                  'Grand Rapids', 'Grande Prairie', 'Graz', 'Great Falls', 'Greece', 'Green Bay', 'Greenland', 
#         'Greenville', 'Grenada', 'Grenoble', 'Griffith', 'Groningen', 'Guadalajara', 'Guadeloupe', 
#                  'Guam', 'Guangzhou', 'Guantanamo', 'Guatemala City', 'Guatemala', 'Guayaquil',
#                  'Guernsey', 'Guilin', 'Guinea', 
# 'Gulfport', 'Gustavus', 'Guwahati', 'Guyana', 'Gwadar', 'Gwangju', 'Hagerstown', 'Haikou',
#                  'Hailey', 'Haiti', 'Halifax', 'Hamburg', 'Hamilton Island', 'Hamilton', 'Hana', 
#                  'Hancock', 'Hangzhou', 'Hannover', 'Hanoi', 'Harare', 'Harbin', 'Hargeisa',
#                  'Harlingen', 'Harrisburg', 'Hartford', 'Havana', 'Hayden', 'Hayman Island', 
#                  'Hays', 'Helena', 'Helsinki', 'Herat', 'Hermosillo', 'Hervey Bay', 'High Level',
#                  'Hilo', 'Hilton Head', 'Hiroshima', 'Ho Chi Minh City', 'Hobart', 'Honduras',
#                  'Hong Kong', 'Honolulu', 'Houston', 'Hubli', 'Hue', 'Humberside', 'Hungary',
#                  'Huntsville', 'Hurghada', 'Huron', 'Hyderabad', 'Ibiza', 'Iceland', 'Idaho Falls',
#                  'Iguazu', 'Ikaria', 'Imperial', 'India', 'Indianapolis', 'Indonesia', 'Indore', 
#                  'Innsbruck', 'Inverness', 'Ipoh', 'Iqaluit', 'Iran', 'Iraq', 'Ireland', 'Iringa',
#                  'Isfahan', 'Islamabad', 'Islay', 'Isles Of Scilly', 'Islip', 'Israel', 'Istanbul',
#                  'Italy', 'Ithaca', 'Ivory Coast', 'Izmir', 'Jackson', 'Jacksonville', 'Jaipur', 
#                  'Jakarta', 'Jamaica', 'Jamestown', 'Jammu', 'Japan', 'Jeddah', 'Jeju', 'Jerez',
#                  'Jersey', 'Jinan', 'Jodhpur', 'Johannesburg', 'Johor Bahru', 'Jonesboro', 'Joplin', 
#                  'Jordan', 'Jos', 'Juba', 'Juneau', 'Kabul', 'Kaduna', 'Kagoshima', 'Kalamata', 
#                  'Kalamazoo', 'Kalgoorlie', 'Kalibo', 'Kaliningrad', 'Kamloops', 'Kandahar', 
#                  'Kano', 'Kansas City', 'Kaohsiung', 'Kapalua', 'Karachi', 'Kars', 'Kasama', 
#                  'Kashi', 'Kathmandu', 'Katowice', 'Kayseri', 'Kazakhstan', 'Kazan', 'Kearney', 
#                  'Kefalonia', 'Kelowna', 'Kenya', 'Kerman', 'Kerry', 'Key West', 'Khajuraho',
#                  'Kharkov', 'Khartoum', 'Khon Kaen', 'Kiev', 'Kigali', 'Kilimanjaro', 'Killeen',
#                  'Kimberley', 'King Salmon', 'Kingsport', 'Kingston', 'Kinshasa', 'Kiribati', 
#                  'Kirov', 'Kisumu', 'Kitale', 'Knock', 'Knoxville', 'Kobe', 'Kochi', 'Kodiak', 
#                  'Kolkata', 'Komatsu', 'Kona', 'Konya', 'Kos', 'Kota Bharu', 'Kota Kinabalu', 'Krabi',
#                  'Krakow', 'Krasnodar', 'Krasnoyarsk', 'Kristiansand', 'Kuala Lumpur', 'Kuantan', 'Kuching', 
#                  'Kudat', 'Kumamoto', 'Kumasi', 'Kunming', 'Kuwait', 'Kyrgyzstan', 'La Coruna', 'La Crosse',
#                  'La Palma', 'La Paz', 'La Romana', 'La Serena', 'Lafayette', 'Lagos', 'Lahore', 'Lake Charles',
#                  'Lampedusa', 'Lamu', 'Lands End', 'Langkawi', 'Lanseria', 'Lansing', 'Lanzarote', 'Laos', 'Lar',
#                  'Laramie', 'Laredo', 'Larnaca', 'Las Vegas', 'Latakia', 'Latvia', 'Launceston', 'Laurel', 
#                  'Lawton', 'Lebanon', 'Leeds', 'Legaspi', 'Leh', 'Leipzig', 'Leon', 'Lesotho', 'Lethbridge', 
#                  'Leticia', 'Lewiston', 'Lexington', 'Lhasa', 'Liberia', 'Libreville', 'Libya', 'Liege', 'Lille', 
#                  'Lilongwe', 'Lima', 'Limoges', 'Lincoln', 'Linz', 'Lisbon', 'Lismore', 'Lithuania', 'Little Rock',
#                  'Liverpool', 'Livingstone', 'Ljubljana', 'Lleida', 'Lodz', 'Loja', 'London', 'Long Beach', 
#                  'Long Island', 'Lord Howe Island', 'Lorient', 'Los Angeles', 'Los Mochis', 'Louisville', 
#                  'Lourdes', 'Luanda', 'Luang Prabang', 'Lubbock', 'Lucknow', 'Lugano', 'Lusaka', 'Luxembourg',
#                  'Luxor', 'Lviv', 'Lynchburg', 'Lyon', 'Maastricht', 'Macau', 'Mackay', 'Madagascar', 'Madeira',
#                  'Madinah', 'Madison', 'Madrid', 'Madurai', 'Mae Hong Son', 'Makhachkala', 'Malabo', 'Malacca', 
#                  'Malaga', 'Malang', 'Malawi', 'Malaysia', 'Maldives', 'Male', 'Mali', 'Malindi', 'Malmo', 'Malta',
#                  'Mammoth Lakes', 'Manado', 'Manaus', 'Manchester', 'Mandalay', 'Mangalore', 'Manhattan', 'Manila',
#                  'Manta', 'Maputo', 'Mar Del Plata', 'Maracaibo', 'Mardin', 'Maribor', 'Mariupol', 'Marquette',
#                  'Marseille', 'Marshall Islands', 'Marshall', "Martha's Vineyard", 'Martinique', 'Martinsburg',
#                  'Mason City', 'Masterton', 'Mataram', 'Matsuyama', 'Maun', 'Mauritania', 'Mauritius', 'Mazatlan',
#                  'Mcallen', 'Medan', 'Medellin', 'Medford', 'Medicine Hat', 'Melbourne', 'Melilla', 'Memphis',
#                  'Mendoza', 'Menorca', 'Merced', 'Merida', 'Metz', 'Mexicali', 'Mexico City', 'Mexico', 'Miami',
#                  'Micronesia', 'Midland', 'Milan', 'Milos', 'Milwaukee', 'Minneapolis', 'Minot', 'Minsk', 'Miri',
#                  'Miskolc', 'Missoula', 'Miyazaki', 'Moab', 'Mobile', 'Modesto', 'Mogadishu', 'Moldova', 'Moline', 
#                  'Mombasa', 'Monaco', 'Moncton', 'Mongolia', 'Monroe', 'Monrovia', 'Monte Carlo', 'Montego Bay', 
#                  'Montenegro', 'Monterrey', 'Montevideo', 'Montgomery', 'Montpellier', 'Montreal', 'Montrose',
#                  'Montserrat', 'Mora', 'Moree', 'Morelia', 'Morgantown', 'Morocco', 'Moscow', 'Mostar', 'Mosul',
#                  'Mozambique', 'Multan', 'Mulu', 'Mumbai', 'Munich', 'Munster', 'Murcia', 'Murmansk', 'Mus',
#                  'Muscat', 'Muskegon', 'Mwanza', 'Myanmar', 'Mykonos', 'Myrtle Beach', 'Mysore', 'Nadi', 'Naga',
#                  'Nagasaki', 'Nagoya', 'Nagpur', 'Naha', 'Nairobi', 'Najaf', 'Nakhon Si Thammarat', 'Namibia', 
#                  'Nan', 'Nanaimo', 'Nantes', 'Nantucket', 'Naples', 'Narrabri', 'Nashville', 'Nassau', 'Natal', 
#                  'Nauru', 'Navegantes', 'Naxos', 'Nelson', 'Nelspruit', 'Nepal', 'Netherlands', 'Nevis',
#                  'New Bern', 'New Caledonia', 'New Haven', 'New Orleans', 'New Plymouth', 'New York',
#                  'New Zealand', 'Newburgh', 'Newcastle', 'Newport News', 'Newquay', 'Niagara Falls', 'Nicaragua',
#                  'Nice', 'Niger', 'Nigeria', 'Niigata', 'Nikolaev', 'Nis', 'Niue', 'Nome', 'Norfolk', 'North Bay',
#                  'North Bend', 'North Korea',
#                 'North Platte', 'Norway', 'Norwich', 'Nottingham', 'Novosibirsk', 'Nuremberg', 'Nyala', 
#                  'Oakland', 'Oaxaca', 'Oban', 'Odessa', 'Ogle', 'Okayama', 'Okinawa', 
#                  'Oklahoma City', 'Old Crow', 'Omaha', 'Oman', 'Omsk', 'Ontario', 'Oran', 'Orange', 
#                  'Orkney', 'Orland', 'Orlando', 'Osaka', 'Osh', 'Oslo', 'Ottawa', 'Oulu', 'Owensboro',
#                  'Paducah', 'Page', 'Pakistan', 'Palau', 'Palembang', 'Palermo', 'Palm Springs', 'Palma',
#                  'Palmas', 'Palmerston North', 'Palu', 'Pamplona', 'Panama City', 'Panama', 'Paphos', 
#                  'Papua New Guinea', 'Paraguay', 'Paris', 'Parkersburg', 'Parma', 'Paro', 'Paros', 
#                  'Pasco', 'Patna', 'Pau', 'Pecs', 'Pekanbaru', 'Pemba', 'Penang', 'Pensacola', 
#                  'Penticton', 'Peoria', 'Pereira', 'Perm', 'Perpignan', 'Perth', 'Peru', 'Perugia', 
#                  'Peshawar', 'Petersburg', 'Philadelphia', 'Philippines', 'Phnom Penh', 'Phoenix', 
#                  'Phu Quoc', 'Phuket', 'Pietermaritzburg', 'Pisa', 'Pittsburgh', 'Plattsburgh', 'Pocatello',
#                  'Pohang', 'Poland', 'Polokwane', 'Ponce', 'Port Angeles', 'Port Au Prince', 'Port Elizabeth',
#                  'Port Harcourt', 'Port Lincoln', 'Port Macquarie', 'Port Moresby', 'Port Of Spain', 'Portland', 
#                  'Porto Alegre', 'Porto', 'Portugal', 'Posadas', 'Poznan', 'Prague', 'Praia', 'Presque Isle', 
#                  'Prince Albert', 'Prince George', 'Providence', 'Provincetown', 'Provo', 'Puebla', 
#                  'Puerto Princesa', 'Puerto Rico', 'Puerto Vallarta', 'Pula', 'Pullman', 'Pune', 'Punta Arenas', 
#                  'Punta Cana', 'Punta Del Este', 'Pyongyang', 'Qassim', 'Qatar', 'Qingdao', 'Quebec', 
#                  'Queenstown', 'Quetta', 'Quincy', 'Quito', 'Rabat', 'Raipur', 'Ramsgate', 'Ranchi', 
#                  'Rapid City', 'Recife', 'Redding', 'Redmond', 'Regina', 'Rennes', 'Reno', 'Reunion', 'Reus',
#                  'Reykjavik', 'Rhodes', 'Richards Bay', 'Richmond', 'Riga', 'Rimini', 'Rio De Janeiro', 
#                  'Rio Grande', 'Riyadh', 'Roanoke', 'Roatan', 'Rochester', 'Rock Sound', 'Rockhampton', 
#                  'Rockland', 'Roma', 'Romania', 'Rome', 'Rosario', 'Rostock', 'Roswell', 'Rotorua', 'Rotterdam',
#                  'Russia', 'Rutland', 'Rwanda', 'Sacramento', 'Saga', 'Saint George', 'Saint John', 'Saint Lucia',
#                  'Saint Thomas', 'Saipan', 'Sal', 'Salamanca', 'Salt Lake City', 'Salta', 'Salvador', 'Salzburg', 
#                  'Samara', 'Samburu', 'Samoa', 'Samos', 'San Angelo', 'San Antonio', 'San Cristobal', 'San Diego',
#                  'San Francisco', 'San Jose', 'San Juan', 'San Luis Obispo', 'San Pedro', 'San Rafael', 
#                  'San Salvador', 'San Sebastian', "Sana'a", 'Santa Ana', 'Santa Barbara', 'Santa Clara', 
#                  'Santa Cruz Is', 'Santa Cruz', 'Santa Fe', 'Santa Maria', 'Santa Marta', 'Santa Rosa', 
#                  'Santander', 'Santiago de Compostela', 'Santiago', 'Santo Domingo', 'Sanya', 'Sao Paulo',
#                  'Sapporo', 'Sarajevo', 'Sarasota', 'Saratov', 'Sarnia', 'Saskatoon', 'Saudi Arabia', 
#                  'Sault Ste Marie', 'Savannah', 'Seattle', 'Sendai', 'Senegal', 'Seoul', 'Serbia', 'Sevastopol',
#                  'Seville', 'Seychelles', 'Shanghai', 'Shannon', 'Sharjah', 'Sharm El Sheikh', 'Shenzhen', 
#                  'Sheridan', 'Shillong', 'Shiraz', 'Show Low', 'Shreveport', 'Sialkot', 'Sidney', 'Siem Reap', 
#                  'Sierra Leone', 'Singapore', 'Sinop', 'Sion', 'Sioux City', 'Sioux Falls', 'Sitka', 'Sivas', 
#                  'Skiathos', 'Skopje', 'Slovakia', 'Slovenia', 'Sochi', 'Socotra', 'Sofia', 'Sokoto', 'Sola', 
#                  'Solomon Islands', 'Somalia', 'Song Pan', 'South Africa', 'South Bend', 'South Korea', 
#                  'Southampton', 'Spain', 'Split', 'Spokane', 'Springfield', 'Sri Lanka', 'Srinagar', 
#                  'St Etienne', "St John's", 'St Louis', 'St Maarten', 'St Martin', 'St Petersburg', 'St. George',
#                  'Stanley', 'State College', 'Staunton', 'Stavanger', 'Stephenville', 'Stockholm', 'Stornoway', 
#                  'Strasbourg', 'Stuttgart', 'Sucre', 'Sudan', 'Sudbury', 'Sunshine Coast', 'Surabaya', 'Surat', 
#                  'Surigao', 'Suriname', 'Suva', 'Swaziland', 'Sweden', 'Switzerland', 'Sydney', 'Sylhet', 
#                  'Syracuse', 'Syria', 'Syros Island', 'Taba', 'Tabriz', 'Tacloban', 'Taichung', 'Taipei', 
#                  'Taiwan', 'Taiyuan', 'Tajikistan', 'Takoradi', 'Tallahassee', 'Tallinn', 'Tampa', 'Tampere', 
#                  'Tampico', 'Tamworth', 'Tan Tan', 'Tangier', 'Tanzania', 'Tashkent', 'Taupo', 'Tauranga', 
#                  'Tbilisi', 'Tehran', 'Tel Aviv', 'Telluride', 'Tenerife', 'Terrace', 'Tete', 'Texarkana', 
#                  'Thailand', 'The Pas', 'The Valley', 'Thessaloniki', 'Thiruvananthapuram', 'Thompson', 
#                  'Thunder Bay', 'Tianjin', 'Tijuana', 'Timaru', 'Timisoara', 'Tirana', 'Tobago', 'Tobruk', 
#                  'Togo', 'Tokyo', 'Toledo', 'Tonga', 'Toowoomba', 'Toronto', 'Torreon', 'Toulon', 'Toulouse', 
#                  'Tours', 'Townsville', 'Toyama', 'Trabzon', 'Trail', 'Traverse City', 'Trieste', 
#                  'Trinidad and Tobago', 'Trinidad', 'Tripoli', 'Tromso', 'Trondheim', 'Trujillo', 'Truk', 
#                  'Tucson', 'Tulsa', 'Tunisia', 'Tupelo', 'Turin', 'Turkey', 'Turkmenistan', 
#                  'Turks and Caicos Islands', 'Turku', 'Tuticorin', 'Ube', 'Udaipur', 'Udon Thani',
#                  'Ufa', 'Uganda', 'Ukraine', 'Ulsan', 'United Arab Emirates', 'United Kingdom', 
#                  'United States', 'Uruguay', 'Ushuaia', 'Uzbekistan', 'Vadodara', 'Vail', 'Valdosta', 
#                  'Valencia', 'Valladolid', 'Valparaiso', 'Van', 'Vancouver', 'Vanuatu', 'Varanasi', 'Varna', 
#                  'Venezuela', 'Venice', 'Veracruz', 'Vernal', 'Verona', 'Victoria Falls', 'Victoria', 
#                  'Vienna', 'Vieques', 'Vietnam',
#                  'Vigo', 'Vijayawada', 'Vilnius', 'Virgin Gorda', 'Virgin Islands', 'Visakhapatnam', 'Vitoria', 
#                  'Vladivostok', 'Volgograd', 'Waco', 'Wagga Wagga', 'Wales', 'Wanaka', 'Warri', 
#                  'Warsaw', 'Washington', 'Waterford', 'Waterloo', 'Watertown', 'Wausau', 'Wellington', 
#                  'West Palm Beach', 'Westchester County', 'Westport', 'Whitehorse', 'Wichita Falls', 
#                  'Wichita', 'Wick', 'Wilkes-Barre', 'Wilmington', 'Windhoek', 'Windsor', 'Winnipeg', 
#                  'Winston-Salem', 'Winton', 'Wroclaw', 'Wuhan', 'Wuxi', 'Xi An', 'Xiamen', 'Yakima', 'Yangon',
#                  'Yap', 'Yellowknife', 'Yemen', 'Yeosu', 'Yerevan', 'Yogyakarta', 'Youngstown', 'Yuma', 'Zagreb',
# 'Zambia' , 'Zamboanga', 'Zanzibar', 'Zaragoza', 'Zimbabwe', 'Zurich')
# i = 'Brazil'
# for (i in destinations){
#   file <- paste('../tidydata/joined/', i, sep='')
#   file <- paste(file, '.csv',sep='')
#   data <- read.csv(file)
#   
#   keeps <- c( "RMCount", "Date", "NSearches")
#   data <- data[(names(data) %in% keeps)]
#   
#   data <- data[complete.cases(data), ]
#   data$Date <- as.Date(data$Date,format="%Y-%m-%d")
#   
#   df <- melt(data, id.vars=c("Date"))
#   
#   ggobj = ggplot(data=df, aes(x=Date, y=value, colour = varible, group=variable))+
#     geom_line(colour = '#00BFFF', size=1) + facet_grid(variable ~ ., scales="free") +
#     scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
#     ggtitle(paste(paste("Plot of ", i, sep=''), " tweets and searches over time", sep=''))+
#     ylab("Searches and Tweets") + 
#     xlab(paste('Normalised searches to and tweets about ', i, sep='')) +
#     theme(axis.text.x=element_text(size=15))
#   #  scale_x_date(labels = date_format("%m-%Y"))
#   print(ggobj)
#   
#   ggsave(sprintf("plots/%s.pdf", i), width=9, height=10)
#   
# }



library(ggplot2)
library(reshape)
library(scales)

setwd('Dev/HonsProject/Work/Rscripts')


destinations = c('Sochi', 'North Korea', 'Brazil', 'Sevastopol', 'Fukuoka', 'Venezuela', 'Ukraine', 'Uruguay')
for (i in destinations){
  file <- paste('../tidydata/joined/', i, sep='')
  file <- paste(file, '.csv',sep='')
  data <- read.csv(file)
  
  keeps <- c( "Count", "Date", "Searches")
  data <- data[(names(data) %in% keeps)]
  

  data$Date <- as.Date(data$Date,format="%Y-%m-%d")
  
  df <- melt(data, id.vars=c("Date"))
  
  ggobj = ggplot(data=df, aes(x=Date, y=value, colour = varible, group=variable))+
    geom_line(colour = '#00BFFF', size=1) + facet_grid(variable ~ ., scales="free") +
    scale_color_manual(values=c("#4B0082", "#FF6347", '#9ACD32', '#EE82EE')) + 
    ggtitle(paste(paste("Plot of ", i, sep=''), " tweets and searches over time", sep=''))+
    ylab("Searches and Tweets") + 
    xlab(paste('Normalised searches to and tweets about ', i, sep='')) +
    theme(axis.text.x=element_text(size=15), axis.text.y = element_blank())
    #scale_x_date(labels = date_format("%m-%Y"))
  print(ggobj)
  
  ggsave(sprintf("plots/%s.pdf", i), width=9, height=10)
}