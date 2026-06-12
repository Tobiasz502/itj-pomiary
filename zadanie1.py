import nidaqmx

# 1. Definiujemy, gdzie makieta jest podłączona (zgodnie z Twoim NI MAX)
kanal_ai = "myDAQ2/ai0"       # Pokrętło (Analog Input)
kanal_di = "myDAQ2/port0/line0" # Przełącznik (Digital Input)

print("Uruchamiam jednorazowy pomiar z urządzenia myDAQ2...")

try:
    # 2. Otwieramy "drzwi" do komunikacji ze sprzętem
    with nidaqmx.Task() as task_ai, nidaqmx.Task() as task_di:
        
        # 3. Mówimy maszynie, z których portów chcemy czytać
        task_ai.ai_channels.add_ai_voltage_chan(kanal_ai)
        task_di.di_channels.add_di_chan(kanal_di)

        # 4. Pobieramy DOKŁADNIE PO JEDNEJ PRÓBCE (wymóg Zadania 1)
        probka_ai = task_ai.read()
        probka_di = task_di.read()

        # 5. Wyświetlamy wyniki w terminalu
        print("\n--- WYNIKI POMIARU ---")
        print(f"Analog Input (Napięcie): {probka_ai:.3f} V")
        
        if probka_di:
            print("Digital Input (Stan): Włączony (Pstryczek w górze)")
        else:
            print("Digital Input (Stan): Wyłączony (Pstryczek w dole)")

except Exception as e:
    print(f"\nBłąd komunikacji ze sprzętem: {e}")
    print("Sprawdź, czy zielona makieta myDAQ2 jest dobrze podpięta do USB!")