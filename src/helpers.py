from bs4 import BeautifulSoup
from win10toast import ToastNotifier
import time
import requests
import look_ups

# main_menu() --------------------------------------------------------------------------------------
# -> Gets user input to determine how they would like to use the program.
def main_menu():
    print(look_ups.line)
    print(look_ups.main_ques)
    for opt in look_ups.menu:
        print(str(opt) + " -> " + look_ups.menu[opt])
    print(look_ups.line)

    ans = input("Option (1-3): ")

    # Ensure proper user input.
    while (not ans.isnumeric()) or (int(ans) > 3 or int(ans) < 1):
        print(look_ups.line)
        print(look_ups.main_ques_err)
        ans = input("Option (1-3): ")

    return int(ans)
# --------------------------------------------------------------------------------------------------

# get_gpu_model() ----------------------------------------------------------------------------------
# -> Gets user input to determine the model of GPU that they would like to check.
def get_gpu_model():
    print(look_ups.line)
    print(look_ups.gpu_ques)
    for gpu in look_ups.gpu_models:
        print(str(gpu) + " -> " + look_ups.gpu_models[gpu])
    print(look_ups.line)

    model = input("GPU Model (0-8): ")

    # Ensure proper user input.
    while (not model.isnumeric()) or (int(model) > 8 or int(model) < 0):
        print(look_ups.line)
        print(look_ups.gpu_ques_err)
        model = input("GPU Model (0-8): ")

    return int(model)
# --------------------------------------------------------------------------------------------------

# get_brands_yn() ----------------------------------------------------------------------------------
# -> Gets user input to determine if they want to only check specific GPU brands.
def get_brands_yn():
    print(look_ups.line)
    print(look_ups.brand_yn_ques)
    print(look_ups.line)

    ans = input("Y/N: ")

    # Ensure proper user input.
    while (ans != "Y") and (ans != "N"):
        print(look_ups.line)
        print(look_ups.brand_yn_ques_err)
        ans = input("Y/N: ")

    if ans == "Y":
        return True
    return False
# --------------------------------------------------------------------------------------------------

# get_brands(x) ------------------------------------------------------------------------------------
# -> Gets user input to determine the GPU brands that they would like to check.
def get_brands(custom):
    if custom:
        print(look_ups.line)
        print(look_ups.brand_ques)
        for brand in look_ups.gpu_brands:
            print(str(brand) + " -> " + look_ups.gpu_brands[brand])
        print(look_ups.line)
        
        brands = input("Brands [0-6]: ")
        # Call the helper function to parse the user input.
        brands_formatted = check_brand_format(brands)

        # Ensure proper user input.
        while len(brands_formatted) == 0:
            print(look_ups.line)
            print(look_ups.brand_ques_err)
            brands = input("Brands [0-6]: ")
            brands_formatted = check_brand_format(brands)
        
        return brands_formatted
    # Return all the brand mappings if False is passed in as the parameter.
    return [1, 2, 3, 4, 5, 6]
# --------------------------------------------------------------------------------------------------

# check_stock(x,y) ---------------------------------------------------------------------------------
# -> Iterate through all the GPUs based on the parameters model & brands. Print out the stock and 
#    product information that is pulled from the site.
def check_stock(model, brands):
    print(look_ups.line)
    # Call on a helper function to get proper formatting for the printed out title.
    tf_1, tf_2 = title_formatting(model)
    print(tf_1 + look_ups.gpu_models[model] + " Stock Levels" + tf_2)

    # Iterate over all the desired GPUs.
    gpu_list = look_ups.can_comp[model]
    for brand in brands:
        if gpu_list[brand] != []:
            print(look_ups.line)
            print("     " + look_ups.gpu_brands[brand])
            print(look_ups.line)
            for gpu in gpu_list[brand]:
                # Construct the link and get the content available at that link.
                link = look_ups.cc_link_1 + gpu_list[0] + look_ups.cc_link_2 + gpu
                site = requests.get(link, headers=look_ups.headers)
                bs = BeautifulSoup(site.content, "lxml")

                # Get the item and part information of the GPU.
                gpu_info = bs.find("div", {"class": "row pb-1"}).find_all("p")
                gpu_item_num = gpu_info[0].text.partition(":")[-1].lstrip()
                gpu_part_num = gpu_info[1].text.partition(":")[-1].lstrip()
                print("Item #: " + gpu_item_num + "    |    Part #: " + gpu_part_num)

                # Get the stock/availability of the GPU at every location/store.
                stock_info = bs.find("div", {"class": "stocklevel-pop"})
                store_stock_info = stock_info.find_all("div", {"class": "col-md-4 col-sm-6"})
                in_stock = 0
                for store in store_stock_info:
                    # Only print information, if the GPU is in stock.
                    if (store.find("p").text != "") and (store.find("span").text != "-"):
                        print("    " + store.find("p").text + ": " + store.find("span").text)
                        in_stock = 1

                # If it is out of stock, print an out of stock message.
                if in_stock == 0:
                    print(look_ups.oos)
    print(look_ups.line)
# --------------------------------------------------------------------------------------------------

# begin_notifier(x,y) ------------------------------------------------------------------------------
# -> Iterate through all the GPUs based on the parameter model. Print out the stock and product 
#    information that is pulled from the site every "timer" minutes. Send the user a notification if 
#    any of the GPUs are available. Loop infinitely.
def begin_notifier(model, timer):
    print(look_ups.line)
    # Call on a helper function to get proper formatting for the printed out title.
    tf_1, tf_2 = title_formatting(model)
    print(tf_1 + look_ups.gpu_models[model] + " Notification" + tf_2)

    # The program should loop infinitely, only stopping by user intervention.
    while True:
        print(look_ups.line)
        # Get the current time so that the program can provide time stamps of stock checks.
        cur_time = time.strftime("(%I:%M:%S %p) [%Z] %b %d, %Y")
        print("Time Stamp of Last Check: " + cur_time)

        # Iterate over all the desired GPUs.
        total_stock = 0
        gpu_list = look_ups.can_comp[model]
        brand_list = [1, 2, 3, 4, 5, 6]
        for brand in brand_list:
            if gpu_list[brand] != []:
                for gpu in gpu_list[brand]:
                    # Construct the link and get the content available at that link.
                    link = look_ups.cc_link_1 + gpu_list[0] + look_ups.cc_link_2 + gpu
                    site = requests.get(link, headers=look_ups.headers)
                    bs = BeautifulSoup(site.content, "lxml")

                    # Get the stock/availability of the GPU at every location/store.
                    stock_info = bs.find("div", {"class": "stocklevel-pop"})
                    store_stock_info = stock_info.find_all("div", {"class": "col-md-4 col-sm-6"})
                    in_stock = 0
                    brand_name = look_ups.gpu_brands[brand]
                    for store in store_stock_info:
                        # Only print information if the GPU is in stock.
                        if (store.find("p").text != "") and (store.find("span").text != "-"):
                            # Get the item and part information of the GPU.
                            gpu_info = bs.find("div", {"class": "row pb-1"}).find_all("p")
                            gpu_item_num = gpu_info[0].text.partition(":")[-1].lstrip()
                            gpu_part_num = gpu_info[1].text.partition(":")[-1].lstrip()
                            # Provide the item + part information only once at the start.
                            if in_stock == 0:
                                print(look_ups.line)
                                print(brand_name + "    |    Item #: " + gpu_item_num + "    |   " \
                                      " Part #: " + gpu_part_num)
                            in_stock = in_stock + 1
                            print(store.find("p").text + ": " + store.find("span").text)
                    total_stock = total_stock + in_stock
                    if in_stock > 0:
                        print(look_ups.line)
        
        # Have a Windows 10 Notification pop up if any of the GPUs were deemed to be in stock.
        if total_stock > 0:
            notification = ToastNotifier()
            notification.show_toast("GPU Stock Notification", "One of the GPUs you were tracking " \
                                    "is currently in stock!", duration=15)
        
        # Let the user know the check was performed, and have the program sleep until the next one.
        print("Last Check Complete. Next check will occur after " + str(timer) + " minutes.")
        time.sleep(timer*60)
# --------------------------------------------------------------------------------------------------

# check_brand_format(x) ----------------------------------------------------------------------------
# -> Given a string, determine if it contains valid brands, and return them.
def check_brand_format(brand_list):
    # Split the string on whitespace.
    brands = brand_list.split()
    i = 0
    while i < len(brands):
        if (not brands[i].isnumeric()) or (int(brands[i]) < 1) or (int(brands[i]) > 6):
            brands.pop(i)
        else:
            i = i + 1
    # Return a list of the brand mappings (1-6) in int format with all duplicates removed. 
    return list(map(int, list(dict.fromkeys(brands))))
# --------------------------------------------------------------------------------------------------

# title_formatting(x) ------------------------------------------------------------------------------
# -> Given a model, return the proper title formatting. 
def title_formatting(model):
    if model == 0 or model == 1 or model == 2 or model == 4:
        return "------------------------- [", "] -------------------------"
    elif model == 3:
        return "------------------------ [", "] -----------------------"
    elif model == 5 or model == 6 or model == 8:
        return "------------------------- [", "] ------------------------"
    else:
        return "-------------------------- [", "] --------------------------"
# --------------------------------------------------------------------------------------------------