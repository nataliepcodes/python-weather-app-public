from datetime import datetime

def main():
    local = datetime.now()
    local_datestamp = local.strftime("%d/%m/%Y") # including the time: ("%d/%m/%Y %H:%M:%S")
    weekday = f'{local.strftime("%A")}'

    result = f'{weekday.upper()} {local_datestamp}'
    return result

"""if __name__ == '__main__':
    main()"""