from TikTokApi import TikTokApi
import string
import random
import json
import os
from datetime import date


def query_keyword_fresh(keyword):

    # call API to initialize search
    verify_fp = "7C66fa6af63ea9408e735663146791fe394c8ae88aef0898735b3a35662d4dbe3f"
    did = ''.join(random.choice(string.digits) for num in range(19))

    api = TikTokApi(custom_verifyfp= verify_fp, use_test_endpoints=True, custom_device_id=did)
            

    # generate directory to store the daily data
    today = date.today()
    d = today.strftime("%d%m%Y")

    new_path = os.path.join("output", (d + "_fresh"))
    os.mkdir(new_path)

    user_list = list()

    # search videos by keyword
    search = api.search()
    tiktoks = search.videos(search_term=keyword, count=500)
    count = 0

    for video in tiktoks:
        count += 1
        if count % 20 == 0:
            print(str(count) + " users processed.")

        # create a sub-directory for each user and all of their profile videos
        user = video.author.username
        subdir_path = os.path.join(new_path, user)
        if os.path.isdir(subdir_path) == True:
            pass
        else:
            os.mkdir(subdir_path)
            print("Creating " + subdir_path)

            # add user to list of scraped users for that day
            user_list.append(user)

            # create JSON object for orignal trending topic video and write to file
            or_vid_path = os.path.join(subdir_path, ("OrigSearch_" + str(video.id) + ".json"))

            json_obj_vid = json.dumps(video.as_dict, indent = 4)
            with open(or_vid_path, 'w') as o:
                o.write(json_obj_vid)
            o.close()

            # search and save user information to JSON file
            user_path = os.path.join(subdir_path, (video.author.username + ".json"))

            user = video.author.info_full()
            json_obj_user = json.dumps(user, indent = 4)
            
            with open(user_path, 'w') as ou:
                ou.write(json_obj_user)
            ou.close()

            # search most recent 100 videos for each user
            user_api = api.user(username= video.author.username)

            for user_video in user_api.videos():

                # save video information to JSON file
                user_vid_path = os.path.join(subdir_path, (str(user_video.id) + ".json"))

                json_obj_uservid = json.dumps(user_video.as_dict, indent = 4)
                with open(user_vid_path, 'w') as ouv:
                    ouv.write(json_obj_uservid)
                ouv.close()
                

    # write list of users to file
    with open(("users_" + d), 'w') as uf:
        uf.write("\n".join(user_list))
    uf.close()


def query_past_users(user_path):

    # generate directory to store the daily data
    today = date.today()
    d = today.strftime("%d%m%Y")

    new_path = os.path.join("output", (d + "_past_" + user_path.split("/")[-2].split("_")[0]))
    os.mkdir(new_path)

    with open(user_path, 'r') as uf:
        lines = uf.readlines()
    uf.close()

    user_list = lines.split("\n")

    # call API to initialize search
    verify_fp = "7C66fa6af63ea9408e735663146791fe394c8ae88aef0898735b3a35662d4dbe3f"
    did = ''.join(random.choice(string.digits) for num in range(19))

    api = TikTokApi(custom_verifyfp= verify_fp, use_test_endpoints=True, custom_device_id=did)

    for username in user_list:
        # search most recent 100 videos for each user
        user_query = api.user(username= username)

        # create a sub-directory for each user and all of their profile videos
        subdir_path = os.path.join(new_path, username)
        os.mkdir(subdir_path)

        # search and save user information to JSON file
        user_path = os.path.join(subdir_path, (username + ".json"))

        user = user_query.info_full()
        json_obj_user = json.dumps(user, indent = 4)
        
        with open(user_path, 'w') as ou:
            ou.write(json_obj_user)
        ou.close()

        for user_video in user.videos(count=100):

            # save video information to JSON file
            user_vid_path = os.path.join(subdir_path, (str(user_video.id) + ".json"))

            json_obj_uservid = json.dumps(user_video.as_dict, indent = 4)
            with open(user_vid_path, 'w') as ouv:
                ouv.write(json_obj_uservid)
            ouv.close()


#query_keyword_fresh("Ukraine")

verify_fp = "7C66fa6af63ea9408e735663146791fe394c8ae88aef0898735b3a35662d4dbe3f"
verify_fp = "verify_l0h968tt_tJaLyZVQ_zzlh_4FLw_AGr2_GWMXn8c8XmRv"
did = ''.join(random.choice(string.digits) for num in range(19))
api = TikTokApi(custom_verifyfp= verify_fp, use_test_endpoints=True)
            
user = api.user(username="philipdefranco")

for video in user.videos():
    print(video.id)