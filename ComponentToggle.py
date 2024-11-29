import os
import glob

# Define the name of the .ini file
file_name = [file for file in glob.glob("*.ini") if not file.lower().startswith("disabled") and not file.lower().startswith("backup")][0]
chara_ibs = [file[:-3] for file in glob.glob("*.ib") if not file.lower().startswith("disabled")]

charaname = file_name[:-4]         
charaparts = []
for i in range(len(chara_ibs)):
    print(str(i)+" - "+chara_ibs[i])
partstotoggle = input("Please enter the index of the parts with toggles, separate with a comma\n")
partstotoggle = [chara_ibs[int(index.strip())] for index in partstotoggle.split(",")]
searching = False
skip = -1
activeWritten = False
partscounter = 0
partstoremove = []
toggleWrite = False
hasActive = False
hasConstants = False

# Check if the file exists in the current directory
if os.path.exists(file_name):
    # Open and read the .ini file line by line
    with open(file_name) as file:
        lines = file.readlines()
    
else:
    print(f"Error: '{file_name}' not found in the current directory.")

for i in range(len(lines)):
    if '[' in lines[i] and ']' in lines[i] and searching:
        searching = False
    if('TextureOverride' in lines[i] and any(part in lines[i] for part in partstotoggle) and any('ib = ' in lines[i + offset] for offset in range(1, 6) if i + offset < len(lines))):
        searching = True

    if ('drawindexed = ' in lines[i] and 'drawindexed = 0, 0, 0' not in lines[i] and searching):
        if('; ' in lines[i-1] and "(" in lines[i-1]):
            charaparts.append(lines[i-1].split(' (')[0].strip()[2:])
    if '$active' in lines[i]:
        hasActive = True
          
with open(f'DISABLED_BACKUPNOTOGGLE_{charaname}.ini', "w") as file:
        for i, line in enumerate(lines):      
            file.write(line)   

with open(f'{charaname}.ini', "w") as file:
        wait = False
        textureoverrideposition = 9999999
        for i, line in enumerate(lines):
            if toggleWrite:
                file.write("if $" +charaparts[partscounter].replace(".", "") + "== 1\n")
                file.write(line)
                file.write("endif\n")
                partscounter+=1
                toggleWrite = False
            else:
                file.write(line)      
            if partscounter<len(charaparts) and ("; " + charaparts[partscounter] + " (") in line:
                toggleWrite = True

            if skip>0:
                skip-=1
            if "; Constants" in line:
                file.write("[Constants]\n")
                if hasActive == False:
                    file.write("global $active = 0\n")
                for part in charaparts:
                    if(input("Creating variable for "+part+", enter skip to skip\n").strip().lower() != "skip"):
                        if(input("Should part be inactive by default? Y/N\n").strip().lower() == 'y'):
                            file.write("global persist $"+ part.replace(".", "") +" = 0\n")
                        else:
                            file.write("global persist $"+ part.replace(".", "") +" = 1\n")
                    else:
                        partstoremove.append(part)

                for part in partstoremove:
                    charaparts.remove(part)

                file.write("\n[Present]\npost $active = 0\n")
                for part in charaparts:
                    file.write("\n")
                    file.write("[Key"+part.replace(".", "")+"]\n")
                    file.write("key = " + input("Please enter key to use for the " + part + "\n")+ "\n")
                    file.write("condition = $active == 1\n")
                    file.write("type = cycle\n")
                    file.write("$"+part.replace(".", "")+"= 0,1\n")
            if hasActive == False:
                if "TextureOverride" in line and "Texcoord" in line and activeWritten == False:
                    skip = 1
                if skip == 0:
                    file.write("$active = 1\n")
                    skip=-1
                    activeWritten = True