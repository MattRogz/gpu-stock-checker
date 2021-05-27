import helpers

# main() -------------------------------------------------------------------------------------------
# -> Runs at start to allow user to choose which program/function they would like to use.
def main():
    # Get user input to figure out which program/function to run.
    choice = helpers.main_menu()
    if choice == 1:
        stock_notifier()
    elif choice == 2:
        stock_checker()
    return
# --------------------------------------------------------------------------------------------------

# stock_notifier() ---------------------------------------------------------------------------------
# -> Takes user input for a GPU model, and displays stock/availability information every 20 minutes.
#    User will be notified via a Windows 10 Notification if any are found in stock.
def stock_notifier():
    model = helpers.get_gpu_model()
    helpers.begin_notifier(model, 20)
# --------------------------------------------------------------------------------------------------

# stock_checker() ----------------------------------------------------------------------------------
# -> Takes user input for a GPU model and brand(s), and displays stock/availability information 
#    at one instance.
def stock_checker():
    model = helpers.get_gpu_model()
    brand_request = helpers.get_brands_yn()
    brands = helpers.get_brands(brand_request)
    helpers.check_stock(model, brands)    
# --------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()