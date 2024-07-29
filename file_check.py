# Read the contents of vids_to_remove.txt
with open('vids_to_remove.txt', 'r') as f:
    vids_to_remove = set(f.read().splitlines())

# Read the contents of vids_to_check.txt
with open('vids_to_check.txt', 'r') as f:
    vids_to_check = set(f.read().splitlines())

# Find the difference
difference = vids_to_remove - vids_to_check

# Write the difference to a new file called difference.txt
with open('difference.txt', 'w') as f:
    for vid in difference:
        f.write(vid + '\n')

print("The differences have been written to difference.txt")
