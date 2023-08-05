testName = "asdf,aadsafsdg, asdfgh, asdf,aadsaf  sdg"
testtemplate = "cypress"
if "cypress" in testtemplate:
    testName = max(testName.split(","), key=len).strip()
print(testName)