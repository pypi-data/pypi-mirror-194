azurefilter = "asdf&asdf&Batch1"

if azurefilter[0:-1].endswith("Batch"):
    azurefilter = azurefilter[0:-7]
print(azurefilter)