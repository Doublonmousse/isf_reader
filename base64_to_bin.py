import base64

base64_text = """
ALQEHQTGBuoKAWBYz1SK5pfFT48G+LrS4Zsi+oeVMvLsF0G4wBa/8yv0er/scczMIrFBiQ67Eyzu
eqFVE2t75fdgSYMf+yvS6VTW3rsTi+Ves0icm6ElWrdREioAGh+LQnBFhHWAvtBF2QQDEEgURID6
/wdFRkcBRvQDUH8FCj0+C09kZWZnaGkZFj0JjTGMMQQAAHpEPgmNMYwxBAAAekRpAxVGAEAKjQOF
AYf0AcegGuOwlAoRIazf7DJ4vDYREpFHpFGplMJhKJdLpZKpJGpBHoRBIVAIVBIXEULgkFi8RhcL
hsVh8ZksblcnlMVnsxjMNj8XhMLgqAweAQKUTCPRybTCNRKKRiGRaIQiERCEQiEQ6GRCAwaCRKGR
KGQiBwuFRKCIDDYVDIHD4NEoMgqAwJB4FBobD4PB4HAoiIbwP5eCAuHgIiOhoiKlq6mwBeTUJIS0
bIxqlqURJysfGxkZAQ8jHw0dAQMLKxUJJRxCxdBQR0XRWEVEQ0JFSUjKw8NFQkTGwMDMzs3Q2djR
zc7IycjGxMvGz8bS0cvIzMbDxcTFwcDBwcZHR8PBxkNGQ8HDSUTAxEpDQMJHQUJFQ0dFQcLGAIL+
I1v4jXAAAAAAAAAAAAAAAAD5fkfX27vJkxPmAACC/iC7+ILwAAAAAAAAAAAAAAAAAAAAAAkICgAR
IFDcVymI0dsBBj6ARAgQAAASABEgmNkwos5F00mp9g9glxEybgMVRgCABRRGAIAAAAMVRgBA
"""

out_file = "decoded.txt"

base64_text = base64_text.replace("\n","")
decoded = base64.b64decode(base64_text)

with open(out_file,"wb") as binary_file:
    binary_file.write(decoded)

# not sure this was 100 % correct ...