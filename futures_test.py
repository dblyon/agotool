import concurrent.futures
import math
from time import sleep 

PRIMES = [
    995095293,
    995942171,
    995095293,
    995190773,
    998077099,
    999285419]

def stupidexample(n):
    counter = 0
    while True:
        if counter > n:
            return counter 
        counter += 1

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(stupidexample, PRIMES)):
            print('%d is me: %s' % (number, prime))


if __name__ == '__main__':
    main()
