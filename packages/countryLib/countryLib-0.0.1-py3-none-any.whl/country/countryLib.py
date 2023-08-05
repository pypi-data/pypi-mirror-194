import httpx


url_full = 'https://restcountries.com/v3.1/name/{}?fullText=true'
url_all = 'https://restcountries.com/v3.1/all'


# Head class
class Country:
	# Init function
	def __init__(self, name: str) -> None:
		self.name = name
		self.response = httpx.get(url_full.format(self.name)).json()
		self.response_all = httpx.get(url_all).json()

	# Return Different types of the country name
	def country_name(self, common_name: bool = True, official_name: bool = False, short_name: bool = False):
		# Store the country name
		list_: list = []

		# If common name is True
		if common_name:
			list_.append((self.response[0]['name']['common']))

		# If official name is True
		if official_name:
			list_.append((self.response[0]['name']['official']))

		# If short name is True
		if short_name:
			list_.append((self.response[0]['altSpellings'][0]))

		# Else nothing given
		if len(list_) == 0:
			return None

		# Return the information
		return tuple(i for i in list_)

	# Reply answers for is... questions
	def is_(self, independent: bool = True, landlocked: bool = False, un_member: bool = False):
		# Answer collection
		list_ = []

		# Check for is independent
		if independent:
			list_.append(self.response[0]['independent'])

		# Check for is landlocked
		if landlocked:
			list_.append(self.response[0]['landlocked'])

		# Check for is United Nation's member
		if un_member:
			list_.append(self.response[0]['unMember'])

		# Return if nothing chosen
		if len(list_) == 0:
			return None

		# Return the answer
		return tuple(i for i in list_)

	# Currency information of the country
	def currency(self, currency: bool = True, name: bool = False, symbol: bool = False):
		# Answer collection
		list_ = []

		# Show short name of the currency
		if currency:
			for i in self.response[0]['currencies'].keys():
				list_.append(i)

		# Show name of the currency
		if name:
			for i in self.response[0]['currencies'].values():
				list_.append(i['name'])

		# Show symbol of the currency
		if symbol:
			for i in self.response[0]['currencies'].values():
				list_.append(i['symbol'])

		# Return None if no currency information
		if len(list_) == 0:
			return None

		# Return the answer
		return tuple(i for i in list_)

	# Phone number of the country
	def phone(self, root: bool = True, suffix: bool = False):
		# Answer collector
		list_ = []

		# Show root of the phone
		if root:
			list_.append(self.response[0]['idd']['root'])

		# Show suffix of the phone
		if suffix:
			list_.append([i for i in self.response[0]['idd']['suffixes']])

		# Return None if no answer
		if len(list_) == 0:
			return None

		# Return the answer
		return tuple(i for i in list_)

	# Language of the country
	def language(self):
		# Answer collector
		list_ = []

		# Get the answer
		for i in self.response[0]['languages'].values():
			list_.append(i)

		# Return the answer
		return tuple(i for i in list_)

	# Map of the country
	def map(self, g_map: bool = True, borders: bool = False, area: bool = False):
		# Answer collector
		list_ = []

		# Google maps
		if g_map:
			list_.append(self.response[0]['maps']['googleMaps'])

		# Borders of the country
		if borders:
			for i in self.response[0]['borders']:
				for j in httpx.get(url_all).json():
					if j['cca3'] == i.upper():
						name = j['name']['common']
						dict_ = {i: name}
						list_.append(dict_)

		if area:
			list_.append(self.response[0]['area'])

		# Return none if there are no infos asked
		if len(list_) == 0:
			return tuple(None, )

		# Return answer
		return tuple(i for i in list_)

	# Domain name of the country
	def domain_name(self):
		# Answer collector
		list_ = []
		list_.append(self.response[0]['tld'][0])

		return tuple(i for i in list_)

	# Capital city of the country
	def capital_city(self):
		return tuple(i for i in self.response[0]['capital'])

	# Flag of the country
	def flag(self):
		return (self.response[0]['flags']['png'],)

	# Car number of the country
	def car(self, signs: bool = True, side: bool = False):
		list_ = []

		if signs:
			list_.append([i for i in self.response[0]['car']['signs']][0])

		if side:
			list_.append(self.response[0]['car']['side'])

		if len(list_) == 0:
			return None

		return tuple(i for i in list_)

	# Time zone of the country
	def time_zone(self):
		return tuple(i for i in self.response[0]['timezones'])

	# Continent of the country
	def continent(self, continent: bool = True, sub_continent: bool = False):
		list_ = []

		if continent:
			list_.append(self.response[0]['region'])

		if sub_continent:
			list_.append(self.response[0]['subregion'])

		if len(list_) == 0:
			return None

		return tuple(i for i in list_)

	# Coat of arm of the country
	def coat_of_arm(self):
		return (self.response[0]['coatOfArms']['png'],)

	# Start of week in the country
	def start_of_week(self):
		return (self.response[0]['startOfWeek'],)

	def all_info(self, common_name: bool = True, official_name: bool = False, short_name: bool = False,
				 phone: bool = False, border: bool = False, area: bool = False, landlocked: bool = False,
				 independent: bool = False, un_member: bool = False, continent: bool = False, time_zone: bool = False,
				 flag: bool = False, currency: bool = False, currency_symbol: bool = False, currency_name: bool = False,
				 capital: bool = False, start_of_week: bool = False, coat_of_arm: bool = False, car_sign: bool = False,
				 all: bool = False):

		list_ = []
		if all:
			common_name = True
			official_name = True
			short_name = True
			phone = True
			border = True
			area = True
			landlocked = True
			independent = True
			un_member = True
			continent = True
			time_zone = True
			flag = True
			currency = True
			currency_symbol = True
			currency_name = True
			capital = True
			start_of_week = True
			coat_of_arm = True
			car_sign = True

			if common_name:
				list_.append(self.country_name())

			if official_name:
				list_.append(self.country_name(common_name=False, official_name=True))

			if short_name:
				list_.append(self.country_name(common_name=False, short_name=True))

			if phone:
				list_.append(self.phone(suffix=True))

			if border:
				list_.append(self.map(g_map=False, borders=True))

			if landlocked:
				list_.append(self.is_(independent=False, landlocked=True))

			if independent:
				list_.append(self.is_())

			if un_member:
				list_.append(self.is_(independent=False, un_member=True))

			if continent:
				list_.append(self.continent())

			if time_zone:
				list_.append(self.time_zone())

			if flag:
				list_.append(self.flag)

			if currency:
				list_.append(self.currency())

			if currency_symbol:
				list_.append(self.currency(currency=False, symbol=True))

			if currency_name:
				list_.append(self.currency(currency=False, name=True))

			if capital:
				list_.append(self.capital_city())

			if start_of_week:
				list_.append(self.start_of_week())

			if coat_of_arm:
				list_.append(self.coat_of_arm())

			if car_sign:
				list_.append(self.car())

			if area:
				list_.append(self.map(g_map=False, area=True))

			return tuple(i for i in list_)

		if common_name:
			list_.append(self.country_name())

		if official_name:
			list_.append(self.country_name(common_name=False, official_name=True))

		if short_name:
			list_.append(self.country_name(common_name=False, short_name=True))

		if phone:
			list_.append(self.phone(suffix=True))

		if border:
			list_.append(self.map(g_map=False, borders=True))

		if landlocked:
			list_.append(self.is_(independent=False, landlocked=True))

		if independent:
			list_.append(self.is_())

		if un_member:
			list_.append(self.is_(independent=False, un_member=True))

		if continent:
			list_.append(self.continent())

		if time_zone:
			list_.append(self.time_zone())

		if flag:
			list_.append(self.flag())

		if currency:
			list_.append(self.currency())

		if currency_symbol:
			list_.append(self.currency(currency=False, symbol=True))

		if currency_name:
			list_.append(self.currency(currency=False, name=True))

		if capital:
			list_.append(self.capital_city())

		if start_of_week:
			list_.append(self.start_of_week())

		if coat_of_arm:
			list_.append(self.coat_of_arm())

		if car_sign:
			list_.append(self.car())

		if area:
			list_.append(self.map(g_map=False, area=True))

		return tuple(i for i in list_)

	def all_countries(self, number: int = 5, name: bool = True, population: bool = False, area: bool = False):
		list_ = []

		if name:
			c = 0
			for i in self.response_all:
				d = {
					i['name']['common']: {
						"official": i['name']['official'],
						"short": i['cca3']
					}
				}

				list_.append(d)
				c += 1
				if c == number:
					break

		if population:
			c = 0
			for i in self.response_all:
				d = {
					i['name']['common']: {
						"population": i['population']
					}
				}

				list_.append(d)
				c += 1
				if c == number:
					break

		if area:
			c = 0
			for i in self.response_all:
				d = {
					i['name']['common']: {
						"area": f"{i['area']}km2"
					}
				}

				list_.append(d)
				c += 1
				if c == number:
					break

	def by_continent(self, continent: bool = True, name: bool = False, number: int = 5):
		list_ = []

		if continent:
			conAsia = []
			conNorth_America = []
			conSouth_America = []
			conAfrica = []
			conEurope = []
			conOceania = []
			conAntarctica = []
			for i in self.response_all:
				if i['continents'][0].lower() == "asia":
					conAsia.append(i['name']['common'])

				if i['continents'][0].lower() == "north america":
					conNorth_America.append(i['name']['common'])

				if i['continents'][0].lower() == "south america":
					conSouth_America.append(i['name']['common'])

				if i['continents'][0].lower() == "africa":
					conAfrica.append(i['name']['common'])

				if i['continents'][0].lower() == "europe":
					conEurope.append(i['name']['common'])

				if i['continents'][0].lower() == "oceania":
					conOceania.append(i['name']['common'])

				if i['continents'][0].lower() == "antarctica":
					conAntarctica.append(i['name']['common'])

			d = {
				"Asia": conAsia,
				"North America": conNorth_America,
				"South America": conSouth_America,
				"Europe": conEurope,
				"Africa": conAfrica,
				"Oceania": conOceania,
				"Antarctica": conAntarctica
			}

			if name:
				try:
					return tuple(d.get(name.title()))[:number]
				except NameError:
					return None

			for i in d.values():
				list_.append(i[:number])
			return tuple(i for i in list_)
		return

