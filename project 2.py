# input: a csv file name
# output:a dictionary of regions with their standard error of population and cosine similarity between population and land area, and a nested dictionary that stores countries within each region along with their population-related information
# name:Yiren Wang (Bohr)
# UWA student ID: 23794201 
# create a function called countrydatafileread to read and store the file
def countrydatafileread(Fileread):
    # create an empty list to hold the parsed data
    countcsv = []
    # create an empty set to hold duplicate country names
    duplicate_countries = set()

    try:
        # open the file for reading
        with open(Fileread, 'r') as countrydatafile:
            # read the header line and split it into lowercase fields
            head = countrydatafile.readline().strip().lower().split(',')

            # find the indices of each field we're interested in
            # assign the index of column header "country" to "country_idx"
            country_idx = head.index('country')

            # assign the index of column header "population" to "population_idx"
            population_idx = head.index('population')

            # assign the index of column header "yearly change" to "Year_idx"
            Year_idx = head.index('yearly change')

            # assign the index of column header "net change" to "net_idx"
            Net_idx = head.index('net change')

            # assign the index of column header "urban" to "Urban_idx"
            Urban_idx = head.index('urban')

            # assign the index of column header "land" to "Land_idx"
            Land_idx = head.index('land area')

            # assign the index of column header "med age" to "age_idx"
            age_idx = head.index('med age')

            # assign the index of column header "regions" to "Regins_idx"
            Regins_idx = head.index('regions')

            # iterate over each line in the file
            for countryline in countrydatafile:
                # split the line into fields and assign them to "data"
                data = countryline.strip().split(',')

                # extract the fields we're interested in
                # assign the index of column with the index "country_idx" to the variable "country"
                country = data[country_idx].lower()

                # assign the index of column with the index "population_idx" to the variable "population"
                population = data[population_idx]

                # assign the index of column with the index "Year_idx" to the variable "year"
                year = data[Year_idx]

                # assign the index of column with the index "Net_idx" to the variable "net"
                net = data[Net_idx]

                # assign the index of column with the index "Urban_idx" to the variable "Urban"
                Urban = data[Urban_idx]

                # assign the index of column with the index "Land_idx" to the variable "Land"
                Land = data[Land_idx]

                # assign the index of column with the index "age_idx" to the variable "age"
                age = data[age_idx]

                # assign the index of column with the index "Regins_idx" to the variable "Region"
                Region = data[Regins_idx].lower()

                # create a list of the extracted fields
                row = [country, population, year, net, Urban, Land, age, Region]

                # check that the row contains valid data (not all empty or None)
                if row[-1] != "" or row[-1] is not None or row[0] != "" or row[0] is not None:
                    # check if we've already seen this country (by name)
                    if not any(r[0] == country for r in countcsv):
                        # if not, add the row to our list
                        countcsv.append(row)
                    else:
                        duplicate_countries.add(country)

        # filter out the duplicate country rows
        countcsv = [row for row in countcsv if row[0] not in duplicate_countries]

        # create a new list without duplicate country rows
        unique_countcsv = []
        for row in countcsv:
            if row[0] not in duplicate_countries:
                unique_countcsv.append(row)

        # sort the list by region
        unique_countcsv.sort(key=lambda line: line[-1])

        # return the parsed data (unique_countcsv)
        return unique_countcsv

    # check if the input file does not exist and return empty dictionary
    except FileNotFoundError:
        return {}
    # check if cannot read the file and return empty dictionary
    except IOError:
        return {}

# create a function SDcos to calculate standard error and cosine similarity
def SDcos(unique_countcsv):
    
    # Create empty dictionaries for storing population, land area, and cosine similarity data
    population_SD, Population_Cos, Land_area = {}, {}, {}
    
    # Loop through each line in the input CSV file
    for line in unique_countcsv:
        
        # Extract the region from the line
        region = line[7]
        
        # using try to testing the anti-bugging
        try:
            
            # Extract the population values from the line, and convert them to floats
            # assign it inthe population_in_range
            population_in_range = float(line[1])
            
            # Extract the Land_area_num values from the line, and convert them to floats
            # assign it inthe population_in_range
            Land_area_num = float(line[5])
            
        # check if the values are not valid floats
        except ValueError:
            return {}
        
        # check if either the population or land area values are <= 0
        if population_in_range <= 0 or Land_area_num <= 0:
            
            # if it is, skip the next line
            continue 
        
        # If the region has not been encountered before
        if region not in population_SD:
            
            # add the region to the "population_SD", "Population_Cos", "Land_area" dictionaries
            population_SD[region],Population_Cos[region],Land_area[region] = [], [], []
        
        # Add the population values to "population_SD" dictionary for the current region
        population_SD[region].append(population_in_range)
        
        # Add the population values to "Population_Cos" dictionary for the current region
        Population_Cos[region].append(population_in_range)
        
        # Add the land area values to "Land_area" dictionary for the current region
        Land_area[region].append(Land_area_num)
    
    # Calculate the standard error for each region based on its population data
    StandardError = {}
    
    # go through the key and value in the dictionary of population_SD one by one, and assign the value called Region and population_in_region
    for Region, population_in_region in population_SD.items():
        
        # find the value number in the population_SD, and store it in the variable of Lenth_of_population
        lenth_of_population = len(population_in_region)
        
        # Calculate the mean population value for the region
        population_mean = sum(population_in_region) / lenth_of_population
        
        # Calculate the deviation from the mean for each population value
        deviations = [(x - population_mean) ** 2 for x in population_in_region]
        
        # Calculate the standard error using the deviations and the number of population values
        ster = round(((sum(deviations) / ( lenth_of_population - 1 )) ** 0.5 ) / lenth_of_population ** 0.5 , 4)
        
        # store the result of standard error and assign to each certain regopn key in the dictionary
        StandardError[Region] = ster
        
    # Calculate the cosine similarity for each region based on its population and land area data
    CosineSimilarity = {}
    
    # go through the key and value in the dictionary of Population_Cos one by one, and assign the value called Region and population_in_region_cos
    for Region, population_in_region_cos in Population_Cos.items():
        
        # assign the key of dictionary in the list of Land_area_list_region
        Land_area_list_region = Land_area[Region]
        
        # Calculate the norm (length) of the population vectors for the region
        norm_population = (sum([x ** 2 for x in population_in_region_cos])) ** 0.5
        
        # Calculate the norm (length) of the Land area vectors for the region
        norm_Land_area = (sum([y ** 2 for y in Land_area_list_region ])) ** 0.5
        
        # Calculate the dot product of the population and land area vectors for the region
        nominator = sum([x * y for x,y in zip(population_in_region_cos,Land_area_list_region)])
        
        # Calculate the cosine similarity using the dot product and the norms of the vectors
        cosine = round( nominator / (norm_Land_area * norm_population) , 4)
        
        # store the result of cosine similarity and assign to each certain regopn key in the dictionary
        CosineSimilarity[Region] = cosine
        
    # Create a dictionary containing the standard error and cosine similarity values for each region
    SdCos = {key:[StandardError[key],CosineSimilarity[key]] for key in StandardError}
    
    # return the result dictionary
    return SdCos

# create a density function to calculate some information for the country including the density-related information
def density(unique_countcsv):

    # create an empty dictionary to store density data
    density_data = {}

    #using for loop to go through each row in the countcsv file
    for line in unique_countcsv:

        # Extract the region from the line
        region = line[7]

        # Extract the country from the first element in the row
        country = line[0]

        #using try to do the anti-bugging
        try:

            # Convert population value to float
            population = float(line[1])

            # Convert net change value to float
            net_change = float(line[3])

            # Convert land area value to float
            Land_area = float(line[5])

        # check if the the file have empty or error value
        except ValueError:
            return {}
        
        # check if the population value is not greater than 0
        # check if the Land_area value is not smaller greater than 0
        if population <= 0 or Land_area <= 0:

            # skip the entire value
            continue 

        # Calculate population percentage relative to the total population of the region
        population_percent = round(population * 100 / sum([float(line[1]) for line in unique_countcsv if line[7].lower() == region.lower()]), 4)

        # Calculate country density (population divided by land area)
        country_density = round(population / Land_area, 4)

        # check the region is not in the density_data dictionary        
        if region not in density_data:

            # add the region value into the dictionary
            density_data[region] = {}

        # Store the population, net change, population percentage, country density, and initial rank in density_data
        density_data[region][country] = [population,net_change,population_percent,country_density,0]

    # go through every region in the density_data dictionary    
    for region in density_data:

        # set the default number of ranking to be 1
        rank = 1

        # Store the population, net change, population percentage, country density, and initial rank in density_date  
        country_ranking = sorted(density_data[region].keys(), key=lambda x: (-density_data[region][x][0], -density_data[region][x][3], x))

        # go through each country name in the dictionary of country_ranking
        for country in country_ranking:

            # re-assign the newwest number of ranking into the fourth value in the country dictionary
            density_data[region][country][4] = rank

            # add 1 unit for ranking
            rank += 1
            
    # return the output 
    return density_data
    
# create a main function with a parameter called "csvfile" to connect all the function above
def main(csvfile):
    
    # Read and process the countrydatafileread function with the CSV file
    # store the result in the variable called regiondata
    regiondata = countrydatafileread(csvfile)

    # call the SDcos funtion with the regiondata
    # assign the output into the variable called dict1
    dict1 = SDcos(regiondata)

    # call the density function with regiondata
    # assign the output intp the cariable called regiondata
    dict2 = density(regiondata)

    # return the output of dict1 and dict 2
    return dict1, dict2

