import csv
print("Convert txt to csv file")
# Define file paths
input_file = 'routes.txt'
output_file = 'routes.csv'

# Read from the text file and write to a CSV file
with open(input_file, mode='r') as txt_file:
    with open(output_file, mode='w', newline='') as csv_file:
        reader = csv.reader(txt_file)
        writer = csv.writer(csv_file)
        for row in reader:
            writer.writerow(row)

print(f"Conversion complete! '{input_file}' has been converted to '{output_file}'.")
