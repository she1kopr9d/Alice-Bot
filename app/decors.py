# def safe_callback(func):
#     @functools.wraps(func)
#     async def inner1(*args, **kwargs):
#         try:
#             await func(*args, **kwargs)
#         except Exception as error:
#             print(error)
#             await menu.inline_main_menu(args[0].message, text="данные устарели")
#     return inner1

# def safe_message(func):
#     @functools.wraps(func)
#     async def inner1(*args, **kwargs):
#         try:
#             await func(*args, **kwargs)
#         except Exception as error:

#     return inner1