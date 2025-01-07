import csv

input_file = 'employ_dep_load.csv'
output_file = 'employ_dep_load_processed.csv'

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile, delimiter=';')
    
    for row in reader:
        id = row[0]
        for person in row[1:]:
            parts = person.split()
            if len(parts) == 3:
                last_name, first_initial, middle_initial = parts
                writer.writerow([id, last_name, first_initial, middle_initial])

print(f"Processed data has been saved to {output_file}")
