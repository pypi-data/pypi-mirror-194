def print_quake(last):
    import colorama
    color = None
    if float(last['Magnitude']) <= 3.9:
        color = colorama.Fore.WHITE
    elif float(last['Magnitude']) <= 5.9:
        color = colorama.Fore.YELLOW
    else:
        color = colorama.Fore.RED
    print(f"\n---\nDeprem oldu!\n---\nYer: {last['Location']}\nBüyüklük:", color, f"{last['Magnitude']}", colorama.Fore.WHITE, f"\nDerinlik: {last['Depth']}\nTarih/Zaman: {last['Date']}/{last['Time']}\n---\n")

def del_one_line():
    print("                                                                                           ", end='\r')