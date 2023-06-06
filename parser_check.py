import difflib


def closest_command(input_string, command_list):
    if input_string.lower() not in command_list:
        suggestion = difflib.get_close_matches(input_string, command_list, cutoff=0.55)
        if suggestion:
            return f"Невідома команда. Можливо ви мали на увазі: {', '.join(suggestion)}."
        else:
            return "Невідома команда."

