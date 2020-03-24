import csv

# Authors: Rana Chan and Colton Paul
# Last modified: 11/1/2018

# This script takes the follow csv's and writes out a new csv that maps Archival Objects (AOs) to Digital Objects (DOs) in ArchivesSpace
# DAM_csv should have the following headers/information: DAM_ID, filename or accession number (depending on what matches with the component unique id in ASpace)
# AS_csv should have the following headers: ref_ID, component_unique_id (csv created from MS EAD export using aspace_xml_to_csv_wtitle.py)
# AS_DO_csv can be the unaltered digital object report from ASpace

# Uncomment the following if you want to have the user specify the path to the csvs
# DAM_csv = raw_input("Path to DAM export CSV: ") #eg. /Users/Jerry/Desktop/python/AS_tests/2018-11-01_DAM_in.csv
# AS_csv = raw_input("Path to ArchivesSpace export CSV: ")
# AS_DO_csv = raw_input("Path to Digital Object export CSV from ASpace: ")
# AS_DAM_link_csv = raw_input("Path to new linked DAM and AS CSV: ") #eg. /Users/Jerry/Desktop/python/AS_tests/2018-11-01_linked_AO_DO_output.csv

# Make sure that your filenames are exactly as they are written below! If you want the user to specify the file, use the block above
DAM_csv = 'DAM_in.csv'
AS_csv = 'AS_in.csv'
AS_DO_csv = 'AS_DO_in.csv'
AS_DAM_link_csv = 'linked_DAM_AS_test.csv'

# This function converts csv files to arrays by taking a csv file as input (must be read in as a csv using open()) and returning an array 
# containing all the contents of each row of the csv
def csv_to_array(csvfile):
    return_array = []
    reader = csv.reader(csvfile)
    for row in reader:
        return_array.append(row)
    return return_array

def main():
    # If using a Windows computer, 'rb' may have to be replaced by 'r' and 'wb' by 'w' and encoding="UTF-8" added
    with open(DAM_csv, 'r', encoding="UTF-8") as csv_dam, open(AS_csv, 'r', encoding="UTF-8") as csv_as, open(AS_DO_csv, 'r', encoding="UTF-8") as csv_as_do, open(AS_DAM_link_csv, 'w') as csvout:
        as_do_lines = csv_to_array(csv_as_do)[1:] # skips header
        dam_lines = csv_to_array(csv_dam)[1:]
        as_csv_lines = csv_to_array(csv_as)[1:]
        
        csvout = csv.writer(csvout, lineterminator='\n') # lineterminator removes the extra empty line between each row
        csvout.writerow(['ref_ID', 'DAM_ID'])
    
        filtered_dam_lines = []

        # Filters the DAM csv array by getting rid of any DOs that have already been linked
        for line in as_do_lines:
            dam_ID_as_do = line[1]
            ms_status = line[4]
            if len(ms_status) == 0: # not linked to AO
                for row in dam_lines:
                    dam_ID_dam = row[0]
                    if dam_ID_as_do == dam_ID_dam:
                        filtered_dam_lines.append(row)
        
        # matches ref_ids to DAM ids using their common metadata: either accession number or filename
        for line in as_csv_lines:
            ref_ID = line[0]
            component_unique_id = line[1]
        
            for row in filtered_dam_lines:
                dam_ID = row[0]
                filename = row[1]
           
                if component_unique_id == filename:
                    csvout.writerow([ref_ID, dam_ID])
                    
if __name__ == "__main__": # runs main()
    main()