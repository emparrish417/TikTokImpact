from TikTokApi import TikTokApi
import sys
import os
 
#print("\nScraping: ", sys.argv[1])

user = "cbsnews"

api = TikTokApi.get_instance()

device_id = api.generate_device_id()

count = 5000

tiktoks = api.by_username(user, count=count)

tikTokNumber = 0
newTikToks = 0

currentDirectory = os.getcwd()

for tiktok in tiktoks:
    tikTokNumber=tikTokNumber+1

    filename = tiktok["id"]+"-"+user+".mp4"
    #CurrentDirectory
    osPath = os.path.join(currentDirectory, filename)
            
    #TikTokUsersDirectory
    dirToCheckOsPath = os.path.join(currentDirectory, user, tiktok["id"]+".mp4")

    if os.path.exists(osPath) or os.path.exists(dirToCheckOsPath):
        print("Already Exists - Continuing : %s - %s" % (filename, tikTokNumber))
    else:
        #Downloads Image
        print("Does Not Exist - Downloding : %s - %s" % (filename, tikTokNumber))
        video_bytes = api.get_video_by_tiktok(tiktok, custom_device_id=device_id)
        with open(osPath, 'wb') as videoFile:
            videoFile.write(video_bytes)

        newTikToks = newTikToks + 1

print("\nFinished Scraping: " +  str(sys.argv[1]) + " | " + str(newTikToks) + " New Tiktoks")