To compile the program run
gcc --std=gnu99 -o tsp tsp2.c -lm

To run the code use
./tsp tsp_example_1
./tsp tsp_example_2 
./tsp tsp_example_3 
./tsp tsp_example_4 
./tsp tsp_example_5 
./tsp tsp_example_6 

To check the code use 
python tsp-verifier.py tsp_example_1 tsp_example_1.txt.tour
python tsp-verifier.py tsp_example_2 tsp_example_2.txt.tour
python tsp-verifier.py tsp_example_3 tsp_example_3.txt.tour
python tsp-verifier.py tsp_example_4 tsp_example_4.txt.tour
python tsp-verifier.py tsp_example_5 tsp_example_5.txt.tour
python tsp-verifier.py tsp_example_6 tsp_example_6.txt.tour

If you are using your own examples the names may change.
./tsp filename
python tsp-verifier.py filename filename.txt.tour
