import json
import datetime
import csv

def domestic_vs_international(low_fares_dict):
	international_cost_sum = 0
	international_total_flights = 0
	domestic_cost_sum = 0
	domestic_total_flights = 0

	#Using only low fares to avoid duplicates seeing as it is the much larger data set
	for k, v in low_fares_dict.items():
		for item in v:
			cost = float(item[5]) + float(item[6])
			if int(item[9]) == 1:
				domestic_cost_sum += cost
				domestic_total_flights += 1
			elif int(item[9]) == 0:
				international_cost_sum += cost
				international_total_flights += 1

	total_flights = domestic_total_flights + international_total_flights
	print("Domestic Flights: {0:6d}".format(domestic_total_flights))
	print("International Flights: {0:6d}".format(international_total_flights))
	print("Total Flights: {0:6d}\n".format(total_flights))
	print("Average Domestic Flight Cost: {0:.2f}".format(float(domestic_cost_sum)/domestic_total_flights))
	print("Average International Flight Cost: {0:.2f}".format(float(international_cost_sum)/international_total_flights))

	return ("Domestic Flights: {0:6d}<br/>Internat'l Flights: {1:6d}<br/>Total Flights: {2:6d} <br/> Avg. Domestic Cost: ${3:.2f}<br/>  Avg. Internat'l Cost: ${4:.2f}".format(
		domestic_total_flights, international_total_flights, total_flights, float(domestic_cost_sum)/domestic_total_flights, float(international_cost_sum)/international_total_flights))



def get_away(deals_dict, low_fares_dict, start_airport):
	lowest_price = 1000000
	best_date = ""
	where_to = ""

	for k, v in deals_dict.items():
		if(k[0] == start_airport):
			for item in v:
				cost = float(item[7]) + float(item[8])
				if cost < lowest_price:
					lowest_price = cost
					best_date = item[3]
					where_to = item[2]

	for k, v in low_fares_dict.items():
		if(k[0] == start_airport):
			for item in v:
				cost = float(item[5]) + float(item[6])
				if cost < lowest_price:
					lowest_price = cost
					best_date = item[2]
					where_to = item[1]

	return "Best Deal from {}: Lowest price: {}| Best date: {}| Destination: {}".format(start_airport, lowest_price, best_date, where_to)


#dollars is bool of if user wants to use dollars or not
def get_cheapest_flights(deals_list, dollars):
	cheapest_flights =[]
	sorted_list = sorted(deals_list, key = lambda flight: flight[6])
	min_price = min(deals_list, key = lambda flight: flight[6])[6]
	for flight in sorted_list:
		if flight[6] == min_price:
			cheapest_flights.append(flight)
		else:
			break
	if dollars:
		return list(filter(lambda flight: flight[5] == 'LOWEST', cheapest_flights))
	else:
		return list(filter(lambda flight: flight[5] != 'LOWEST', cheapest_flights))

def getAirportData(airport_data, name):
	return airport_data[name]

def avgPrice(data_tuple):
	data = data_tuple[1]
	cost_dollar = 0
	cost_points = 0
	valid_flights_dollar = 0
	valid_flights_points = 0
	for flight in data:
		if flight[4] == 'LOWEST':
			cost_dollar += float(flight[5])
			valid_flights_dollar += 1
		elif flight[4] == 'POINTS':
			cost_points += float(flight[7])
			valid_flights_points +=1
	return (0 if(valid_flights_dollar == 0) else cost_dollar/valid_flights_dollar, 0 if(valid_flights_points == 0) else cost_points/valid_flights_points)
	
#Takes in dates as strings
def is_in_date_range(start, end, target):
	uses_slashes = False
	uses_dashes = False

	if target.find('/') != -1:
		uses_slashes = True
	elif target.find('-') != -1:
		uses_dashes = True

	if uses_dashes:
		target = target.split('-')
		target_date = datetime.date(int(target[0]), int(target[1]), int(target[2][:2]))

	elif uses_slashes: 
		target = target.split('/')
		target_date = datetime.date(int(target[2][:4]), int(target[0]), int(target[1]))
		
	start = start.split("/")
	
	end = end.split("/")
	
	start_date = datetime.date(int(start[2]), int(start[0]), int(start[1]))
	end_date = datetime.date(int(end[2]), int(end[0]), int(end[1]))

	return target_date > start_date and target_date < end_date

#Processes information
#Assumes start_date and end_date in form of 'mm/dd/yyyy'
def process(deals, low_fares, left_date, right_date, depart_code, dest_code):
	deals_in_range = []
	lowest_fares_in_range = []
	deal_list = deals[(depart_code,dest_code)]
	low_list = low_fares[(depart_code, dest_code)]
	for flight in deal_list:
		if is_in_date_range(left_date, right_date, flight[3]):
			deals_in_range.append(flight)

	for flight in low_list:
		if is_in_date_range(left_date, right_date, flight[2]):
			lowest_fares_in_range.append(flight)

	return (deals_in_range, lowest_fares_in_range)

def cheapest_route(deals,low_fares,left_date,right_date,depart_code,dest_code):
	#cheapest_direct = get_cheapest_flights(process(deals,low_fares,'0/0/0','12/31/2100',depart_code,dest_code),1)
	min_connect_flight_cost = 99999
	f1 = None
	f2 = None
	found2ndflight = False
	for key,val in deals.items():
		min_f1 = 99999
		if key[0] == depart_code and key[1] != dest_code:
			for item in val:
				if is_in_date_range(left_date,right_date,item[3]) and float(item[7]) <= min_f1:
					min_f1 = float(item[7])
					f1 = item
	for key1,val1 in deals.items():
		min2 = 99999
		if key1[0] == f1[2] and key1[1] == dest_code:
			for item1 in val1:
				if is_in_date_range(left_date,right_date,item1[3]) and float(item1[7]) <= min2:
					min2 - float(item1[7])
					f2 = item1
					found2ndflight = True

	if not found2ndflight:
		return None
	return (f1,f2)




			

	# if(cheapest_direct[0][5] <= min_connect_flight_cost):
	# 	return cheapest_direct

	# else:
	# 	return conn_flight_list
	return conn_flight_list












if(__name__ == "__main__"):
	print("Hello World")
	# print(is_in_date_range('12/01/1998', '12/12/2017', '01/01/2000'))
	# print(is_in_date_range('12/01/2010', '12/12/2017', '01/01/2000'))
