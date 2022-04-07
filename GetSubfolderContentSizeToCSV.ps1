#Written by: Eric Croiset
#Version 1.0
#This script will total all base folder sizes of multiple target root folders and export that information to a ; delimited file.
#MMDB Project - Magic Movie Database

#Set $AlleOrdnerPfade to the target root folders
$AlleOrdnerPfade = @('J:\MMDB\Filme\', 'J:\MMDB\Series', 'L:\MMDB\Movies', 'L:\MMDB\Series')

#Set the target of ; delimited csv file (Currently set to create a file MMDB.csv of the user running the script)
$output = "C:\$ENV:HOMEPATH\Desktop\MMDB.csv"

# Variable to temporarily save the output
$results = @()
$results += 'Foldername;Size in GB'

#First loop for all the target root folders from $AlleOrdnerPfade
foreach ($startFolder in $AlleOrdnerPfade){
    # Gets all the child items from the root folders
    $colItems = (Get-ChildItem $startFolder | Where-Object {$_.PSIsContainer -eq $True})
    
    # Second loop going through all the child items of the root folders ($colItems)
    foreach ($i in $colItems)
        {
            #Write the name of the current child item of the root folder beeing processd
            $i.FullName
            #Get the sum of size of all child items in the child item of the root folder
            $subFolderItems = (Get-ChildItem -Literalpath $i.FullName -recurse | Measure-Object length -sum)
            #Save the output as csv ; delimited line in $results
            $results += $i.FullName + ";" + "{0:N2}" -f ($subFolderItems.sum / 1GB)
        }
}
#write all the results to the previously defined csv file
$results > $output
