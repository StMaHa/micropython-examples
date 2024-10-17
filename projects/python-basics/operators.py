min_wert = 10
max_wert = 20
wert = 15
ist_wert_gueltig = (wert >= min_wert) and (wert <= max_wert)
print(ist_wert_gueltig)  # True
 
wert = 9
ist_wert_gueltig = (wert >= min_wert) and (wert <= max_wert)
print(ist_wert_gueltig)  # False
