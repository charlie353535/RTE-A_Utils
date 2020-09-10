import os,re,shutil

productregex = r"\s?\*\s+Product:  (.*)\s+(Rev\.\s+(\d+))"
productregex2 = r".*Product:  (.*)\s+(Rev\.\s?(\d+)).*"

doneproducts = []
files = []
for file in os.listdir("archive"):
    if not file.endswith(".src"): continue
    #print("processing "+file)
    files.append(file)

files = files[::-1]

for file in files:
    MATCHED = False
    PRODUCT = ""
    REVSTR = ""
    REV = ""
    pl1 = ""
    pl2 = ""
    pl3 = ""
    with open("archive/"+file,"r") as f:
        if "software numbering file" not in f.read().lower(): continue
    with open("archive/"+file,"r") as f:
        for line in f:
            match = re.match(productregex,line,re.IGNORECASE)
            if (match != None): 
                MATCHED = True
                PRODUCT = match.groups()[0].strip()
                REVSTR = match.groups()[1].strip()
                REV = match.groups()[2].strip()
            match = re.match(productregex2,line,re.IGNORECASE)
            if (match != None): 
                MATCHED = True
                PRODUCT = match.groups()[0].strip()
                REVSTR = match.groups()[1].strip()
                REV = match.groups()[2].strip()
            if MATCHED: break
            pl3 = pl2
            pl2 = pl1
            pl1 = line
    if not MATCHED: continue
    if (int(REV) < 3000):
        continue
    if (len(pl2.replace(" ","")) < 4) and len(pl3.replace(" ","").replace("*","")) > 3:
        pl2 = pl3
    if (len(pl2.replace(" ","")) < 4) and len(pl3.replace(" ","").replace("*","")) < 2:
        pl2 = pl1
    pl2 = pl2.upper().replace("Software Numbering File:".upper(),"").replace("Software Numbering File.".upper(),"").replace("Software Numbering File".upper(),"").replace("*","").strip()
    if PRODUCT not in doneproducts:
        print("["+file+"] contains product "+PRODUCT+" revision "+REV+" "+pl2)
        doneproducts.append(PRODUCT)
        shutil.copyfile("archive/"+file,"listings/"+PRODUCT+"_rev_"+REV+"_listing.txt")
