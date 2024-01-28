# Function to calculate the checksum for a TLE line
def calculate_checksum(tle_line):
    # Initialize checksum to zero
    checksum = 0
    # Iterate over each character in the line
    for char in tle_line[:-1]:  # Exclude the last character as it is the checksum itself
        if char.isdigit():
            # Add the integer value of the digit to the checksum
            checksum += int(char)
        elif char == '-':
            # Minus sign counts as 1
            checksum += 1
    # The checksum is the last digit of the sum
    checksum %= 10
    return checksum

# Given TLE lines
tle_line1 = "1 58463U 23185B   24028.57483594  .00003172  00000+0  24716-3 0  9991"
tle_line2 = "2 58463  97.6448  97.5298 0015178  54.5451 305.7188 15.01839645  8677"

# Calculate checksum for each line
checksum_line1 = calculate_checksum(tle_line1)
checksum_line2 = calculate_checksum(tle_line2)

print(checksum_line1)
print(checksum_line2)
