import os,re,shutil
import os.path

cdir = "/"

#file_regex = r"^\s+(.*)\s+(\d+)-(\d+) (\d+)\s+(\d) \w+"
file_regex = r"^\s+(.*)\s+(\d+)-(\d+) (\d+)\s+(\d)"
dir_regex = r"^\s?Directory:\s(.*)$"

types = ["ERROR", ".fbin", ".fbin", "notfound", ".src", ".rbin", ".prog", ".abin"]

def process(listing):
    global cdir
    cdir = "/"
    with open(listing,"r") as f:
        for line in f:
            fmatch = re.match(dir_regex,line)
            if (fmatch != None):
                if (len(fmatch.groups()) == 1):
                    cdir = fmatch.groups()[0].strip()
                    print("DIR "+cdir)
                    if not os.path.exists(".\output\\"+cdir[1:].replace("/","\\")):
                        cdir = cdir.replace("::","");
                        print("MKDIR "+cdir[1:])
                        os.makedirs(".\output\\"+cdir[1:].replace("/","\\"))
            
            match = re.match(file_regex,line)
            if (match == None):
                continue
            groups = match.groups()
            if (groups == None):
                continue
            if (len(groups) != 5): continue
            fromname = groups[1] + "-" + groups[2] + "_Rev-" + groups[3] + types[int(groups[4])]
            if (fromname.endswith("notfound")): continue
            toname = cdir + "/" + groups[0].strip()
            print("COPY ["+fromname+"] => ["+toname[1:].replace("/","\\")+"]")
            if not os.path.exists("archive\\"+fromname):
                print("FILE NOT FOUND: ["+"archive\\"+fromname+"]")
                continue
            shutil.copyfile("archive\\"+fromname,"output\\"+toname[1:].replace("CON.","{CON}.").replace("/","\\").replace("\"","{SM}").replace("<","{LT}").replace(">","{GT}").replace("?","{QM}").replace("*","{ST}"))
            #os.rename(toname,fromname)

for filename in os.listdir("listings"):
    print("******************************************************")
    print("  PROCESSING "+filename)
    print("******************************************************")    
    process("listings\\"+filename)
