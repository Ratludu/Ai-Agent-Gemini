from functions.get_files_info import get_files_info 


tests = {

    "test_1":("calculator","."),
    "test_2":("calculator","pkg"),
    "test_3":("calculator","/bin"),
    "test_4":("calculator","../")
}


for name, params in tests.items():
    print(get_files_info(params[0], params[1]))
