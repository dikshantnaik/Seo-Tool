import sheets

urls = sheets.input_websites()

print(urls)

with open("data.txt","w") as f:
    for url in urls:
        f.write(url+"\n")