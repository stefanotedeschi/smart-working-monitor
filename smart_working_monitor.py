import speedtest as st
import pandas as pd
from datetime import datetime
import schedule
import time
import webbrowser
import win32api
import signal
import platform

def measure_speed():

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print(f"[{now}] Performing Speedtest...")

    speed_test = st.Speedtest()
    speed_test.get_best_server()

    print("\tPing...", end=" ")
    ping = speed_test.results.ping
    print(f"{ping} ms")

    print("\tDownload...", end=" ")
    download = speed_test.download()
    download_mbs = round(download / (10**6), 2)
    print(f"{download_mbs} Mbps")

    print("\tUpload... ", end=" ")
    upload = speed_test.upload()
    upload_mbs = round(upload / (10**6), 2)  
    print(f"{upload_mbs} Mbps") 

    update_csv(now, ping, download_mbs, upload_mbs)


def update_csv(time, ping, download, upload):

    print("\tWriting results...", end='')

    csv_file_name = "internet_speeds.csv"

    # Load the CSV to update
    try:
        csv_dataset = pd.read_csv(csv_file_name, index_col="Date")
    # If there's an error, assume the file does not exist and create\
    # the dataset from scratch
    except:
        csv_dataset = pd.DataFrame(
            list(),
            columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"]
        )

    # Create a one-row DataFrame for the new test results
    results_df = pd.DataFrame(
        [[ping, download, upload]],
        columns=["Ping (ms)", "Download (Mb/s)", "Upload (Mb/s)"],
        index=[time]
    )

    if(csv_dataset.empty):
        updated_df = results_df
    else:
        updated_df = pd.concat([csv_dataset, results_df])
    updated_df\
        .loc[~updated_df.index.duplicated(keep="last")]\
        .to_csv(csv_file_name, index_label="Date")
    
    print("DONE!\n")

def on_exit():
    webbrowser.open('https://forms.gle/FLJw4PzeLukmmsKN9')

def exit_handler_windows(signal_type):
   on_exit()

def exit_handler_unix(signum, frame):
  on_exit()

def main():
    if platform.system() == "Windows":
        win32api.SetConsoleCtrlHandler(exit_handler_windows, True)
    else:
        signal.signal(signal.SIGHUP, exit_handler_unix)
    try:

        print("\n***** SMART WEST - REMOTE WORKING MONITOR *****\n")
        print('''***L'Universita' della Valle d'Aosta sta svolgendo uno studio 
***sulle problematiche tecnologiche collegate allo smart working 
***nei territori montani.\n
***Lo studio e' parte del progetto NODES 
***(Nord Ovest Digitale E Sostenibile, ecs-nodes.eu) finanziato su 
***fondi del PNRR. Le chiediamo, per favore, di dare il consenso 
***alla raccolta e invio di dati sulle performance del suo sistema 
***di connettivita' internet.\n
***L'applicativo raccoglie informazioni su banda e latenza ad intervalli 
***periodici e invia su base giornaliera ad un server gestito dall'Universita' 
***della Valle d'Aosta i dati memorizzati. Le assicuriamo che i dati saranno 
***trattati in modo anonimo nel pieno rispetto della normativa vigente in materia 
***di privacy (Regolamento UE 2016/679 e d.l. n. 101 del 10 agosto 2018).\n
***La ringraziamo per la Sua collaborazione.\n\n''')
        
        measure_speed()
        schedule.every(15).minutes.do(measure_speed)
        while True:
            schedule.run_pending()
            time.sleep(1)
    finally:
        on_exit()

if __name__ == "__main__":
    main()