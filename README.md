# Testowanie VTune

Użyj `python tests/measure_vtune.py` do pozyskania komend, aby uruchomić określone testy w VTune. Skrypt ten generuje komendy, które można skopiować i wkleić do terminala, aby uruchomić testy w VTune.

# Testowanie poprawności

Użyj `python tests/prime_collect.py` do zebrania wygenerowanych liczb pierwszych.
Następnie użyj `python tests/prime_validate.py` do sprawdzenia poprawności wygenerowanych liczb pierwszych.




# Testy wydajności

python.exe .\tests\performance\schedules_K2.py | tee .\outputs_2\schedules_K2.txt
python.exe .\tests\performance\schedules_K4.py | tee .\outputs_2\schedules_K4.txt
python.exe .\tests\performance\schedules_K4a.py | tee .\outputs_2\schedules_K4a.txt
python.exe .\tests\performance\mix_K5.py | tee .\outputs_2\mix_K5.txt